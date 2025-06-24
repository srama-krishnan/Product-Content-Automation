import React, { useState } from 'react';
import './ResBox.css';

const ResBox = ({ data, onRegenerate, isLoading }) => {
  const [editableData, setEditableData] = useState(data);
  const [showEnglish, setShowEnglish] = useState(false);

  const handleChange = (field, value) => {
    setEditableData({ ...editableData, [field]: value });
  };

  const handlePush = () => {
    console.log('✅ Pushed:', editableData);
    alert('✅ Content pushed! (Simulated)');
  };

  return (
    <div className="resbox-container">
      <h3>Generated Product Content</h3>

      <div className="description-columns">
        <div className="desc-section">
          <label>Icelandic Short Description</label>
          <textarea
            rows={3}
            value={editableData.short_description_is}
            onChange={(e) => handleChange("short_description_is", e.target.value)}
          />
        </div>

        {showEnglish && (
          <div className="desc-section">
            <label>English Short Description</label>
            <textarea
              rows={3}
              value={editableData.short_description_en}
              onChange={(e) => handleChange("short_description_en", e.target.value)}
            />
          </div>
        )}
      </div>

      <div className="description-columns">
        <div className="desc-section">
          <label>Icelandic Long Description</label>
          <textarea
            rows={6}
            value={editableData.long_description_is}
            onChange={(e) => handleChange("long_description_is", e.target.value)}
          />
        </div>

        {showEnglish && (
          <div className="desc-section">
            <label>English Long Description</label>
            <textarea
              rows={6}
              value={editableData.long_description_en}
              onChange={(e) => handleChange("long_description_en", e.target.value)}
            />
          </div>
        )}
      </div>

      <button
        onClick={() => setShowEnglish((prev) => !prev)}
        className="english-toggle"
      >
        {showEnglish ? "Hide English Version" : "Check English Version"}
      </button>

      <h4>Technical Specifications</h4>
      <table className="spec-table">
        <thead>
          <tr><th>Key</th><th>Value</th></tr>
        </thead>
        <tbody>
          {Object.entries(editableData.technical_specifications || {}).map(([k, v]) => (
            <tr key={k}>
              <td>{k}</td>
              <td>{v}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="resbox-buttons">
        <button onClick={onRegenerate} disabled={isLoading}>🔁 Re-Generate</button>
        <button onClick={handlePush} disabled={isLoading}>🚀 Push</button>
      </div>
    </div>
  );
};

export default ResBox;
