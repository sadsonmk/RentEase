import React, { useState } from 'react';

function SearchBar() {
    const [searchTerm, setSearchTerm] = useState('');

    const handleSearch = (e) => {
        setSearchTerm(e.target.value);
    };

    return (
        <div className='search_bar'>
            <input 
                type='text'
                placeholder='Search...'
                value={searchTerm}
                onChange={handleSearch}
            />
            <button>Search</button>
        </div>
    );
}

export default SearchBar;