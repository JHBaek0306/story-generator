import React, { useState, useEffect } from "react";

interface ImageUploaderProps {
    setImage : (file: File) => void;
}

export const ImageUploader = ({ setImage }: ImageUploaderProps) => {
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
        setImage(file);
        const url = URL.createObjectURL(file);
        setPreviewUrl(url);
        }
    };

    useEffect(() => {
        return () => {
        if (previewUrl) URL.revokeObjectURL(previewUrl);
        };
    }, [previewUrl]);

    return (
        <div className="previewImg">
            <div className="previewBox">
                {previewUrl ? (
                <img src={previewUrl} alt="Preview" className="img" />
                ) : (
                <div className="placeholder">Upload a image</div>
                )}
            </div>
        <input type="file" accept="image/*" onChange={handleChange} className="fileInput" />
        </div>
    );
};
