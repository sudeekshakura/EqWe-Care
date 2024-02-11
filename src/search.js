
import React, { useState, useEffect } from 'react';
import Uploadfile from './uploadfiles'
function SearchBar({ onSearch }) {
  const [searchTerm, setSearchTerm] = useState('');

  const handleChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearch = () => {
    onSearch(searchTerm);
  };

  return (
    <div style={{ paddingLeft: "1000px" }}>
      <input
        type="text"
        placeholder="Search by ID..."
        value={searchTerm}
        onChange={handleChange}
      />
      <button onClick={handleSearch} style={{ background: "#1976d2", color: "white", marginTop: "20px" }}>Search</button>
    </div>
  );
}

function Table({ data }) {
  return (
    <table style={{ paddingLeft: "1150px", paddingTop: "10px" }}>
      <thead>
        <tr style={{ color: "#1976d2"}}>
          <th>ID</th>
          <th style={{paddingLeft:"30px"}}>Name</th>
          <th style={{paddingLeft:"30px"}}>Age</th>
        </tr>
      </thead>
      <tbody style={{ color: "#1976d2" }}>
        {data && (
          <tr>
            <td>{data.seqn}</td>
            <td style={{paddingLeft:"30px"}}>{data.first}</td>
            <td style={{paddingLeft:"30px"}}>{data.age}</td>
          </tr>
        )}
      </tbody>
    </table>
  );
}

function Search() {
  const [searchResults, setSearchResults] = useState(null);

  const handleSearch = async (id) => {
    try {
      const response = await fetch(`http://localhost:3001/data/${id}`);
      console.log(response)
      const data = await response.json();
      console.log("DATAAAA",data.seqn)
      setSearchResults(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div>
      <SearchBar onSearch={handleSearch} />
      <Table data={searchResults} />
      <Uploadfile data={searchResults}></Uploadfile>
    </div>
  );
}

export default Search;
