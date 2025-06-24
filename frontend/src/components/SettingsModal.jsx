import React, { useState, useEffect } from 'react';
import './SettingsModal.css';

const SettingsModal = ({ initialValues, onClose, onSave }) => {
  const [form, setForm] = useState({
    tone: '',
    temperature: '',
    top_p: '',
    max_tokens: '',
    short_desc_words: '',
    long_desc_words: '',
    keywords: '',
  });

  // Refresh form state when modal is reopened
  useEffect(() => {
    if (initialValues) {
      setForm({
        tone: initialValues.tone || '',
        temperature: initialValues.temperature || '',
        top_p: initialValues.top_p || '',
        max_tokens: initialValues.max_tokens || '',
        short_desc_words: initialValues.short_desc_words || '',
        long_desc_words: initialValues.long_desc_words || '',
        keywords: Array.isArray(initialValues.keywords)
          ? initialValues.keywords.join(', ')
          : initialValues.keywords || '',
      });
    }
  }, [initialValues]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    const finalData = {
      ...form,
      temperature: parseFloat(form.temperature),
      top_p: parseFloat(form.top_p),
      max_tokens: parseInt(form.max_tokens),
      short_desc_words: parseInt(form.short_desc_words),
      long_desc_words: parseInt(form.long_desc_words),
      keywords: form.keywords
        ? form.keywords.split(',').map(k => k.trim()).filter(Boolean)
        : [],
    };
    onSave(finalData);
    onClose();
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
            placeholder="Enter tone"
          />
        </div>

        <div className="modal-input">
          <label>Temperature</label>
          <input
            type="number"
            step="0.1"
            name="temperature"
            value={form.temperature}
            onChange={handleChange}
            placeholder="e.g., 0.7"
          />
        </div>

        <div className="modal-input">
          <label>Top P</label>
          <input
            type="number"
            step="0.1"
            name="top_p"
            value={form.top_p}
            onChange={handleChange}
            placeholder="e.g., 1.0"
          />
        </div>

        <div className="modal-input">
          <label>Max Tokens</label>
          <input
            type="number"
            name="max_tokens"
            value={form.max_tokens}
            onChange={handleChange}
            placeholder="e.g., 800"
          />
        </div>

        <div className="modal-input">
          <label>Short Description Word Limit</label>
          <input
            type="number"
            name="short_desc_words"
            value={form.short_desc_words}
            onChange={handleChange}
            placeholder="e.g., 25"
          />
        </div>

        <div className="modal-input">
          <label>Long Description Word Limit</label>
          <input
            type="number"
            name="long_desc_words"
            value={form.long_desc_words}
            onChange={handleChange}
            placeholder="e.g., 200"
          />
        </div>

        <div className="modal-input">
          <label>Extra Keywords (comma separated)</label>
          <input
            type="text"
            name="keywords"
            value={form.keywords}
            onChange={handleChange}
            placeholder="e.g., smart, waterproof"
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
