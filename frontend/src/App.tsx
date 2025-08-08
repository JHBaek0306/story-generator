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

  const handleGenerate = async () => {
    if (image) {
      const result = await generateStory(image, genre, prompt);
      setStory(result.story);
      setImageCaption(result.image_caption);
      setReflection(result.reflection);
    }
  };

  return (
    <div>
      <div className="one">
        <h1>Story Creater</h1>
      </div>
      <ImageUploader setImage={setImage} />
      <div className="selectGenre">Select Genre</div>
      <GenreSelector genre={genre} setGenre={setGenre} />
      <StoryPromptInput prompt={prompt} setPrompt={setPrompt} onGenerate={handleGenerate}/>
      <StoryDisplay story={story} imageCaption={imageCaption} reflection={reflection} />
    </div>
  );
};

export default App;
