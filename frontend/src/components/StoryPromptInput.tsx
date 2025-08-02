type Props = {
    prompt: string;
    setPrompt: (p: string) => void;
    onGenerate: () => void;
};

export const StoryPromptInput = ({ prompt, setPrompt, onGenerate }: Props) => (
    <div className="storyPromptWrapper">
        <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Please enter additional information..."
        className="storyPromptInput"
        rows={3}
        />
        <button className="generateButton" onClick={onGenerate}>
        Generate Story
        </button>
    </div>
);
