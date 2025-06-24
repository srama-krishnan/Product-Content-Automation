import React, { useState } from 'react';
import './ResBox.css';

const ResBox = ({ data, onRegenerate, isLoading }) => {
  const [editableData, setEditableData] = useState(data);
  const [showEnglish, setShowEnglish] = useState(false);

  const handleChange = (field, value) => {
    setEditableData({ ...editableData, [field]: value });
  };

  const handleSpecChange = (key, value) => {
    const specKey = showEnglish
      ? 'technical_specifications'
      : 'translated_technical_specifications';

    setEditableData({
      ...editableData,
      [specKey]: {
        ...editableData[specKey],
        [key]: value,
      },
    });
  };

  const handlePush = () => {
    console.log('✅ Pushed:', editableData);
    alert('✅ Content pushed! (Simulated)');
  };

  const currentSpecs = showEnglish
    ? editableData.technical_specifications
    : editableData.translated_technical_specifications;
  const handleDownloadJSON = () => {
  const filename = `${editableData.sku || 'product'}_data.json`;
  const blob = new Blob([JSON.stringify(editableData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();

  URL.revokeObjectURL(url);
};

const handleCopyToClipboard = () => {
  const dataToCopy = {
    product_name: editableData.product_name,
    brand: editableData.brand,
    sku: editableData.sku,
    short_description: showEnglish
      ? editableData.short_description_en
      : editableData.short_description_is,
    long_description: showEnglish
      ? editableData.long_description_en
      : editableData.long_description_is,
    technical_specifications: showEnglish
      ? editableData.technical_specifications
      : editableData.translated_technical_specifications,
    keywords: editableData.keywords,
    generated_at: editableData.generated_at,
  };

  navigator.clipboard.writeText(JSON.stringify(dataToCopy, null, 2))
    .then(() => alert(`📋 ${showEnglish ? 'English' : 'Icelandic'} JSON copied to clipboard!`))
    .catch(() => alert("❌ Failed to copy JSON"));
};


  return (
    <div className="resbox-container">
      <h3>Generated Product Content</h3>

      <div className="description-columns">
        <div className="desc-section">
          <label>{showEnglish ? 'English Short Description' : 'Icelandic Short Description'}</label>
          <textarea
            rows={2}
            value={
              showEnglish
                ? editableData.short_description_en
                : editableData.short_description_is
            }
            onChange={(e) =>
              handleChange(
                showEnglish ? 'short_description_en' : 'short_description_is',
                e.target.value
              )
            }
          />
        </div>
      </div>

      <div className="description-columns">
        <div className="desc-section">
          <label>{showEnglish ? 'English Long Description' : 'Icelandic Long Description'}</label>
          <textarea
            rows={12}
            value={
              showEnglish
                ? editableData.long_description_en
                : editableData.long_description_is
            }
            onChange={(e) =>
              handleChange(
                showEnglish ? 'long_description_en' : 'long_description_is',
                e.target.value
              )
            }
          />
        </div>
      </div>

      <button
        onClick={() => setShowEnglish((prev) => !prev)}
        className="english-toggle"
      >
        {showEnglish ? 'Show Icelandic Version' : 'Check English Version'}
      </button>

      <h4>Technical Specifications ({showEnglish ? 'English' : 'Icelandic'})</h4>
      <table className="spec-table">
        <thead>
          <tr>
            <th>Key</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(currentSpecs || {}).map(([k, v]) => (
            <tr key={k}>
              <td>{k}</td>
              <td>
                <input
                  type="text"
                  value={v}
                  onChange={(e) => handleSpecChange(k, e.target.value)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="resbox-buttons">
        <button onClick={onRegenerate} disabled={isLoading}>🔁 Re-Generate</button>
        <button onClick={handleCopyToClipboard}>📋 Copy JSON</button>
        <button onClick={handleDownloadJSON}>📥 Download JSON</button>
        <button onClick={handlePush} disabled={isLoading}>🚀 Push</button>
      </div>
    </div>
  );
};

export default ResBox;
