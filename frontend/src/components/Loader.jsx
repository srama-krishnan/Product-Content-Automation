import React from 'react';
import './Loader.css';

const Loader = () => {
  return (
    <div className="loader-wrapper">
      <div className="spinner" />
      <p>Generating product content... Please wait.</p>
    </div>
  );
};

export default Loader;
