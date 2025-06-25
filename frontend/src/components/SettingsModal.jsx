import React, { useState, useEffect } from 'react';
import './SettingsModal.css';

const defaultSettings = {
  tone: '',
  temperature: '0.7',
  top_p: '1.0',
  max_tokens: '800',
  short_desc_words: '25',
  long_desc_words: '200',
  keywords: '',
};

const SettingsModal = ({ initialValues, onClose, onSave }) => {
  const [form, setForm] = useState({ ...defaultSettings, ...initialValues });

  useEffect(() => {
    setForm({ ...defaultSettings, ...initialValues });
  }, [initialValues]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    // Numeric fields validation
    if (['temperature', 'top_p'].includes(name)) {
      if (value === '' || (parseFloat(value) >= 0 && parseFloat(value) <= 1)) {
        setForm({ ...form, [name]: value });
      }
    } else if (['max_tokens', 'short_desc_words', 'long_desc_words'].includes(name)) {
      if (/^\d*$/.test(value)) {
        setForm({ ...form, [name]: value });
      }
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSave = () => {
    const finalData = {
      ...form,
      keywords: form.keywords
        ? form.keywords.split(',').map(k => k.trim()).filter(Boolean)
        : [],
    };
    onSave(finalData);
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-box">
        <h3>Optional Settings</h3>

        <div className="modal-input">
          <label>Tone</label>
          <input
            type="text"
            name="tone"
            value={form.tone}
            onChange={handleChange}
            placeholder="Write professionally and highlight key features"
          />
        </div>

        <div className="modal-input">
          <label>Temperature</label>
          <input
            type="text"
            name="temperature"
            value={form.temperature}
            onChange={handleChange}
          />
          <small className="helper-text">Allowed values: 0.0 – 1.0</small>
        </div>

        <div className="modal-input">
          <label>Top P</label>
          <input
            type="text"
            name="top_p"
            value={form.top_p}
            onChange={handleChange}
          />
          <small className="helper-text">Allowed values: 0.0 – 1.0</small>
        </div>

        <div className="modal-input">
          <label>Max Tokens</label>
          <input
            type="text"
            name="max_tokens"
            value={form.max_tokens}
            onChange={handleChange}
          />
          <small className="helper-text">Positive integers (e.g., 800)</small>
        </div>

        <div className="modal-input">
          <label>Short Description Word Limit</label>
          <input
            type="text"
            name="short_desc_words"
            value={form.short_desc_words}
            onChange={handleChange}
          />
          <small className="helper-text">Recommended: 10 – 50</small>
        </div>

        <div className="modal-input">
          <label>Long Description Word Limit</label>
          <input
            type="text"
            name="long_desc_words"
            value={form.long_desc_words}
            onChange={handleChange}
          />
          <small className="helper-text">Recommended: 100 – 300</small>
        </div>

        <div className="modal-input">
          <label>Keywords (comma separated)</label>
          <input
            type="text"
            name="keywords"
            value={form.keywords}
            onChange={handleChange}
          />
        </div>

        <div className="modal-buttons">
          <button onClick={handleSave}>Save</button>
          <button onClick={onClose} className="cancel">Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;
