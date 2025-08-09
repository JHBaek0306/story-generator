import React from 'react';
import './GenreSelector.css';

interface GenreSelectorProps {
  genre: string;
  setGenre: (genre: string) => void;
}

export const GenreSelector: React.FC<GenreSelectorProps> = ({ genre, setGenre }) => {
  const genres = ["Adventure", "Fantasy", "Sci-fi", "Comedy", "Mystery"];

  return (
    <div className="genre-selector">
      <label htmlFor="genre-select">Choose a genre:</label>
      <div className="custom-select-wrapper">
        <select
          id="genre-select"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          className="genre-select-dropdown"
        >
          {genres.map(genreChoose => (
            <option key={genreChoose} value={genreChoose}>
              {genreChoose}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};
