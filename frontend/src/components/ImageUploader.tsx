import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import './ImageUploader.css';

interface ImageUploaderProps {
  setImage: (file: File) => void;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({ setImage }) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setImage(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  }, [setImage]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: {'image/*':[]} });

  return (
    <div {...getRootProps()} className={`image-uploader ${isDragActive ? 'active' : ''}`}>
      <input {...getInputProps()} />
      {previewUrl ? (
        <img src={previewUrl} alt="Preview" className="image-preview" />
      ) : (
        <div className="placeholder">
          <p>Drag & drop an image here, or click to select one</p>
          <em>(Images up to 10MB)</em>
        </div>
      )}
    </div>
  );
};
