import React from 'react';
import './StoryDisplay.css';

interface StoryDisplayProps {
  story: string;
  imageCaption: string;
  reflection: string;
}

export const StoryDisplay: React.FC<StoryDisplayProps> = ({ story, imageCaption, reflection }) => {
  return (
    <div className="story-display-container">
      {imageCaption && (
        <div className="story-section">
          <h2>Image Caption</h2>
          <p>{imageCaption}</p>
        </div>
      )}
      {story && (
        <div className="story-section">
          <h2>Generated Story</h2>
          <p>{story}</p>
        </div>
      )}
      {reflection && (
        <div className="story-section">
          <h2>Reflection</h2>
          <p>{reflection}</p>
        </div>
      )}
    </div>
  );
};
