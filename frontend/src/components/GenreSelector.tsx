export const GenreSelector = ({
    genre,
    setGenre,
    }: {
    genre: string;
    setGenre: (g: string) => void;
    }) => (
    <div className="genreSelectorContainer">
        <select
        value={genre}
        onChange={(e) => setGenre(e.target.value)}
        className="genreSelect"
        >
        <option value="adventure">Adventure</option>
        <option value="fantasy">Fantasy</option>
        <option value="sci-fi">Sci-Fi</option>
        <option value="comedy">Comedy</option>
        <option value="mystery">Mystery</option>
        </select>
    </div>
);
