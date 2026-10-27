import React from 'react';
import {
  FileText,
  Image as ImageIcon,
  Presentation,
  FileCode,
  File,
} from 'lucide-react';

export default function FileTypeIcon({ type, className = 'w-5 h-5' }) {
  const norm = (type || '').toLowerCase();

  switch (norm) {
    case 'pdf':
      return <FileText className={`${className} text-rose-500`} />;
    case 'image':
    case 'jpg':
    case 'jpeg':
    case 'png':
    case 'webp':
      return <ImageIcon className={`${className} text-amber-500`} />;
    case 'docx':
    case 'doc':
      return <FileText className={`${className} text-blue-500`} />;
    case 'pptx':
    case 'ppt':
      return <Presentation className={`${className} text-orange-500`} />;
    case 'txt':
      return <FileCode className={`${className} text-emerald-500`} />;
    default:
      return <File className={`${className} text-slate-400`} />;
  }
}
