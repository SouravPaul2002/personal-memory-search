import os
import shutil
import tempfile
import time
import unittest
from unittest.mock import patch

import backend.database.database as db_module
from backend.database.schema import initialize_database
from backend.indexing.file_registry import (
    get_all_files,
    get_file
)
from backend.indexing.folder_scanner import scan_custom_folder
import backend.indexing.incremental_scan as inc_scan_module
from backend.utils.file_utils import (
    norm_path,
    is_file_in_dir,
    is_file_in_folders
)

SAMPLE_TEXT = (
    "This is a valid test document containing more than one hundred characters of content "
    "to ensure that the chunking and indexing services can process it cleanly without issues."
)


class TestPathUtils(unittest.TestCase):
    def test_norm_path(self):
        p1 = "D:/test/folder/file.txt"
        p2 = "d:\\test\\folder\\file.txt"
        self.assertEqual(norm_path(p1), norm_path(p2))

    def test_is_file_in_dir_non_recursive(self):
        dir_path = "D:/data/txts"
        direct_file = "D:/data/txts/doc.txt"
        sub_file = "D:/data/txts/sub/doc.txt"
        other_file = "D:/other/doc.txt"

        self.assertTrue(is_file_in_dir(direct_file, dir_path, recursive=False))
        self.assertFalse(is_file_in_dir(sub_file, dir_path, recursive=False))
        self.assertFalse(is_file_in_dir(other_file, dir_path, recursive=False))

    def test_is_file_in_dir_recursive(self):
        dir_path = "D:/data/txts"
        direct_file = "D:/data/txts/doc.txt"
        sub_file = "D:/data/txts/sub/doc.txt"
        other_file = "D:/other/doc.txt"

        self.assertTrue(is_file_in_dir(direct_file, dir_path, recursive=True))
        self.assertTrue(is_file_in_dir(sub_file, dir_path, recursive=True))
        self.assertFalse(is_file_in_dir(other_file, dir_path, recursive=True))

    def test_is_file_in_folders(self):
        folders = ["D:/data/txts", "D:/data/pdfs"]
        self.assertTrue(is_file_in_folders("D:/data/txts/doc.txt", folders, recursive=False))
        self.assertTrue(is_file_in_folders("D:/data/pdfs/doc.pdf", folders, recursive=False))
        self.assertFalse(is_file_in_folders("D:/custom/doc.txt", folders, recursive=False))


class TestCustomFolderAndIncrementalScan(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_files.db")

        # Create standard folders
        self.pdf_folder = os.path.join(self.test_dir, "data", "pdfs")
        self.image_folder = os.path.join(self.test_dir, "data", "images")
        self.txt_folder = os.path.join(self.test_dir, "data", "txts")
        self.docx_folder = os.path.join(self.test_dir, "data", "docx")
        self.pptx_folder = os.path.join(self.test_dir, "data", "pptx")

        for f in [self.pdf_folder, self.image_folder, self.txt_folder, self.docx_folder, self.pptx_folder]:
            os.makedirs(f, exist_ok=True)

        # Create custom folders
        self.custom_folder_a = os.path.join(self.test_dir, "custom_a")
        self.custom_folder_b = os.path.join(self.test_dir, "custom_b")
        os.makedirs(self.custom_folder_a, exist_ok=True)
        os.makedirs(self.custom_folder_b, exist_ok=True)

        # Patch DB path
        self.db_patcher = patch.object(db_module, "DB_PATH", self.db_path)
        self.db_patcher.start()

        # Patch incremental scanner folders
        self.std_folders = [
            self.pdf_folder,
            self.image_folder,
            self.txt_folder,
            self.docx_folder,
            self.pptx_folder
        ]
        self.patch_pdf = patch.object(inc_scan_module, "PDF_FOLDER", self.pdf_folder)
        self.patch_img = patch.object(inc_scan_module, "IMAGE_FOLDER", self.image_folder)
        self.patch_txt = patch.object(inc_scan_module, "TXT_FOLDER", self.txt_folder)
        self.patch_docx = patch.object(inc_scan_module, "DOCX_FOLDER", self.docx_folder)
        self.patch_pptx = patch.object(inc_scan_module, "PPTX_FOLDER", self.pptx_folder)
        self.patch_std = patch.object(inc_scan_module, "STANDARD_FOLDERS", self.std_folders)

        for p in [self.patch_pdf, self.patch_img, self.patch_txt, self.patch_docx, self.patch_pptx, self.patch_std]:
            p.start()

        # Initialize fresh database schema
        initialize_database()

        # Mock Chroma chunk deletion and indexing to isolate test and keep it fast
        def dummy_index_txt(txt_path, filename):
            return {
                "chunks": 1,
                "keywords": ["test", "memory"],
                "topics": ["unit-test"],
                "summary": "Summary of document"
            }

        self.deleted_chunks = []

        def dummy_delete_txt(filename):
            self.deleted_chunks.append(filename)

        self.patch_idx_folder = patch("backend.indexing.folder_scanner.index_txt", side_effect=dummy_index_txt)
        self.patch_del_folder = patch("backend.indexing.folder_scanner.delete_txt_chunks", side_effect=dummy_delete_txt)
        self.patch_idx_inc = patch("backend.indexing.incremental_scan.index_txt", side_effect=dummy_index_txt)
        self.patch_del_inc = patch("backend.indexing.incremental_scan.delete_txt_chunks", side_effect=dummy_delete_txt)

        self.patch_idx_folder.start()
        self.patch_del_folder.start()
        self.patch_idx_inc.start()
        self.patch_del_inc.start()

    def tearDown(self):
        self.patch_del_inc.stop()
        self.patch_idx_inc.stop()
        self.patch_del_folder.stop()
        self.patch_idx_folder.stop()

        for p in [self.patch_std, self.patch_pptx, self.patch_docx, self.patch_txt, self.patch_img, self.patch_pdf]:
            p.stop()
        self.db_patcher.stop()

        # Clean up temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_scenario_1_custom_file_remains_indexed_after_incremental_scan(self):
        """
        Scenario 1:
        Index a file from a custom folder, then run an incremental scan of the standard folders.
        The custom file must remain indexed.
        """
        custom_file = os.path.join(self.custom_folder_a, "custom_doc.txt")
        with open(custom_file, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT)

        # 1. Scan custom folder
        scan_res = scan_custom_folder(self.custom_folder_a)
        self.assertEqual(scan_res["new_files"], 1)
        self.assertEqual(scan_res["errors"], [])

        # Verify indexed in DB
        db_record = get_file(custom_file)
        self.assertIsNotNone(db_record)
        self.assertEqual(db_record["is_deleted"], 0)

        # 2. Run incremental scan of standard storage folders
        inc_res = inc_scan_module.run_incremental_scan()
        self.assertEqual(inc_res["deleted_files"], 0)

        # 3. Custom file MUST remain indexed and active
        db_record_after = get_file(custom_file)
        self.assertIsNotNone(db_record_after)
        self.assertEqual(db_record_after["is_deleted"], 0)

    def test_scenario_2_two_custom_folders_scanning_one_preserves_other(self):
        """
        Scenario 2:
        Index files from two different custom folders, then scan only one folder.
        Files from the other folder must remain indexed.
        """
        file_a = os.path.join(self.custom_folder_a, "doc_a.txt")
        with open(file_a, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " A")

        file_b = os.path.join(self.custom_folder_b, "doc_b.txt")
        with open(file_b, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " B")

        # Index both
        scan_custom_folder(self.custom_folder_a)
        scan_custom_folder(self.custom_folder_b)

        self.assertEqual(get_file(file_a)["is_deleted"], 0)
        self.assertEqual(get_file(file_b)["is_deleted"], 0)

        # Scan only folder A again
        scan_a_again = scan_custom_folder(self.custom_folder_a)
        self.assertEqual(scan_a_again["deleted_files"], 0)

        # File in folder B MUST still be active
        rec_b = get_file(file_b)
        self.assertIsNotNone(rec_b)
        self.assertEqual(rec_b["is_deleted"], 0)

    def test_scenario_3_delete_file_from_custom_folder_and_scan(self):
        """
        Scenario 3:
        Delete a file from a custom folder and scan that folder.
        The deleted file should be handled correctly.
        """
        custom_file = os.path.join(self.custom_folder_a, "to_delete.txt")
        with open(custom_file, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " to delete")

        scan_custom_folder(self.custom_folder_a)
        self.assertEqual(get_file(custom_file)["is_deleted"], 0)

        # Delete file from disk
        os.remove(custom_file)

        # Scan folder A again
        scan_res = scan_custom_folder(self.custom_folder_a)
        self.assertEqual(scan_res["deleted_files"], 1)

        # Check DB status is marked deleted
        rec = get_file(custom_file)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["is_deleted"], 1)
        self.assertIn("to_delete.txt", self.deleted_chunks)

    def test_scenario_4_modify_file_and_scan(self):
        """
        Scenario 4:
        Modify an existing file and scan its folder.
        The index should reflect the updated content.
        """
        custom_file = os.path.join(self.custom_folder_a, "to_modify.txt")
        with open(custom_file, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " v1")

        scan_custom_folder(self.custom_folder_a)
        initial_hash = get_file(custom_file)["content_hash"]

        # Modify content
        time.sleep(0.01)
        with open(custom_file, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " v2 modified")

        scan_res = scan_custom_folder(self.custom_folder_a)
        self.assertEqual(scan_res["modified_files"], 1)
        self.assertEqual(scan_res["new_files"], 0)
        self.assertEqual(scan_res["deleted_files"], 0)

        updated_rec = get_file(custom_file)
        self.assertNotEqual(updated_rec["content_hash"], initial_hash)
        self.assertEqual(updated_rec["is_deleted"], 0)

    def test_scenario_5_repeated_scans_no_duplicates(self):
        """
        Scenario 5:
        Run the same scan multiple times.
        No duplicate file records or vectors should be created.
        """
        custom_file = os.path.join(self.custom_folder_a, "repeat_test.txt")
        with open(custom_file, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " stable custom")

        std_file = os.path.join(self.txt_folder, "standard_doc.txt")
        with open(std_file, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " stable std")

        # Initial scans
        res_custom_1 = scan_custom_folder(self.custom_folder_a)
        self.assertEqual(res_custom_1["new_files"], 1)

        res_inc_1 = inc_scan_module.run_incremental_scan()
        self.assertEqual(res_inc_1["new_files"], 1)

        active_files_1 = get_all_files()
        self.assertEqual(len(active_files_1), 2)

        # Repeated scans without modification
        res_custom_2 = scan_custom_folder(self.custom_folder_a)
        self.assertEqual(res_custom_2["new_files"], 0)
        self.assertEqual(res_custom_2["modified_files"], 0)
        self.assertEqual(res_custom_2["skipped_files"], 1)
        self.assertEqual(res_custom_2["deleted_files"], 0)

        res_inc_2 = inc_scan_module.run_incremental_scan()
        self.assertEqual(res_inc_2["new_files"], 0)
        self.assertEqual(res_inc_2["modified_files"], 0)
        self.assertEqual(res_inc_2["deleted_files"], 0)

        # Total active file records must still be exactly 2
        active_files_2 = get_all_files()
        self.assertEqual(len(active_files_2), 2)

    def test_standard_folder_deletion_reconciled_properly(self):
        """
        Verify that files deleted from standard folders ARE reconciled as deleted.
        """
        std_file = os.path.join(self.txt_folder, "standard_to_del.txt")
        with open(std_file, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " standard delete")

        inc_scan_module.run_incremental_scan()
        self.assertEqual(get_file(std_file)["is_deleted"], 0)

        # Delete from standard folder
        os.remove(std_file)

        res = inc_scan_module.run_incremental_scan()
        self.assertEqual(res["deleted_files"], 1)
        self.assertEqual(get_file(std_file)["is_deleted"], 1)

    def test_reactivate_previously_deleted_file(self):
        """
        Verify that restoring a previously deleted file re-activates it cleanly
        without duplicate records.
        """
        custom_file = os.path.join(self.custom_folder_a, "resurrect.txt")
        with open(custom_file, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " v1")

        scan_custom_folder(self.custom_folder_a)
        self.assertEqual(get_file(custom_file)["is_deleted"], 0)

        os.remove(custom_file)
        scan_custom_folder(self.custom_folder_a)
        self.assertEqual(get_file(custom_file)["is_deleted"], 1)

        # Recreate file
        with open(custom_file, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEXT + " v2 restored")

        res = scan_custom_folder(self.custom_folder_a)
        self.assertEqual(res["new_files"], 1)

        rec = get_file(custom_file)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["is_deleted"], 0)


if __name__ == "__main__":
    unittest.main()
