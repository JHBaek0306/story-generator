interface StoryProps {
    story : string;
}

export const StoryDisplay = ({ story }:StoryProps) => (
    <div className="storyDisplayWrapper">
        <div className="storyDisplayBox">
        <h3>Generated Story</h3>
        <p>{story}</p>
        </div>
    </div>
);
