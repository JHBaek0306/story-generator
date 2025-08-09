import React from 'react';
import './StoryPromptInput.css';

interface StoryPromptInputProps {
  prompt: string;
  setPrompt: (prompt: string) => void;
  onGenerate: () => void;
  loading: boolean;
}

export const StoryPromptInput: React.FC<StoryPromptInputProps> = ({ prompt, setPrompt, onGenerate, loading }) => {
  return (
    <div className="story-prompt">
      <label htmlFor="prompt-textarea">Your creative prompt:</label>
      <textarea
        id="prompt-textarea"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="e.g., a hidden treasure, a bright personality...."
        className="prompt-textarea"
        rows={4}
      />
      <button
        onClick={onGenerate}
        className="generate-button"
        disabled={loading}
      >
        {loading ? 'Generating...' : 'Generate Story'}
      </button>
    </div>
  );
};
