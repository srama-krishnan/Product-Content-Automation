import React, { useState } from 'react';
import './SettingsModal.css';

const SettingsModal = ({ initialValues, onClose, onSave }) => {
  const [form, setForm] = useState({
    tone: initialValues.tone || '',
    temperature: initialValues.temperature || '',
    top_p: initialValues.top_p || '',
    max_tokens: initialValues.max_tokens || '',
    short_desc_words: initialValues.short_desc_words || '',
    long_desc_words: initialValues.long_desc_words || '',
    keywords: initialValues.keywords || '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    // Clean keywords into list if entered
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

        {['tone', 'temperature', 'top_p', 'max_tokens', 'short_desc_words', 'long_desc_words', 'keywords'].map((field) => (
          <div className="modal-input" key={field}>
            <label>{field.replace(/_/g, ' ')}</label>
            <input
              type="text"
              name={field}
              value={form[field]}
              onChange={handleChange}
              placeholder={`Enter ${field}`}
            />
          </div>
        ))}

        <div className="modal-buttons">
          <button onClick={handleSave}>Save</button>
          <button onClick={onClose} className="cancel">Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;
