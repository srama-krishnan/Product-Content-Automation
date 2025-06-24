import React, { useState } from 'react';
import "./InputForm.css"
const InputForm = ({ onGenerate, onOpenSettings, isLoading }) => {
  const [productName, setProductName] = useState('');
  const [brand, setBrand] = useState('');
  const [sku, setSku] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onGenerate({ product_name: productName, brand, sku });
  };

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <div className="input-group">
        <label>Product Name</label>
        <input
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          required
        />
      </div>

      <div className="input-group">
        <label>Brand</label>
        <input
          type="text"
          value={brand}
          onChange={(e) => setBrand(e.target.value)}
          required
        />
      </div>

      <div className="input-group">
        <label>SKU</label>
        <input
          type="text"
          value={sku}
          onChange={(e) => setSku(e.target.value)}
          required
        />
      </div>

      <div className="button-group">
        <button type="submit" disabled={isLoading}>Generate</button>
        <button type="button" onClick={onOpenSettings} disabled={isLoading}>
          Settings
        </button>
      </div>
    </form>
  );
};

export default InputForm;
