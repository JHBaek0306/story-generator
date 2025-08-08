interface StoryProps {
    story : string;
    imageCaption: string;
    reflection: string;
}

export const StoryDisplay = ({ story, imageCaption, reflection }:StoryProps) => (
    <div className="storyDisplayWrapper">
        <div className="storyDisplayBox">
        <h3>Generated Story</h3>
        <p>{story}</p>
        <h3>Image Caption</h3>
        <p>{imageCaption}</p>
        <h3>Reflection</h3>
        <p>{reflection}</p>
        </div>
    </div>
);
