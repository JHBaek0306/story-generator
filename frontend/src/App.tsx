import { useState } from 'react';
import './App.css';
import { GenreSelector } from "./components/GenreSelector";
import { ImageUploader } from "./components/ImageUploader";
import { StoryPromptInput } from "./components/StoryPromptInput";
import { StoryDisplay } from "./components/StoryDisplay";
import { generateStory } from "./utils/api";

const App = () => {
  const [genre, setGenre] = useState("adventure");
  const [prompt, setPrompt] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [story, setStory] = useState("");
  const [imageCaption, setImageCaption] = useState("");
  const [reflection, setReflection] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (image) {
      setLoading(true);
      const result = await generateStory(image, genre, prompt);
      setStory(result.story);
      setImageCaption(result.image_caption);
      setReflection(result.reflection);
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>AI Story Generator</h1>
      </header>

      <div className="input-section">
        <div className="left-panel">
          <ImageUploader setImage={setImage} />
        </div>
        <div className="right-panel">
          <GenreSelector genre={genre} setGenre={setGenre} />
          <StoryPromptInput prompt={prompt} setPrompt={setPrompt} onGenerate={handleGenerate} loading={loading} />
        </div>
      </div>

      {(story || imageCaption || reflection) &&
        <div className="story-display">
          <StoryDisplay story={story} imageCaption={imageCaption} reflection={reflection} />
        </div>
      }
    </div>
  );
};

export default App;
