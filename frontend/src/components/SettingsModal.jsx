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
    keywords: Array.isArray(initialValues.keywords)
      ? initialValues.keywords.join(', ')
      : initialValues.keywords || '',
  });

  const tooltips = {
    tone: "Tone sets the style of writing.\nEg: playful, professional.",
    temperature: "Controls randomness.\nLow = focused, High = creative.",
    top_p: "Alternative to temperature.\nLower = more focused text.",
    max_tokens: "Total word length limit.\nHigher = longer response.",
    short_desc_words: "Word limit for short desc.\nKeep small for punchy texts.",
    long_desc_words: "Word limit for long desc.\nHigher = more detailed.",
    keywords: "Optional boost words.\nE.g., durable, eco-friendly.",
  };

  const fieldLabels = {
    tone: "Tone",
    temperature: "Temperature",
    top_p: "Top P",
    max_tokens: "Max Tokens",
    short_desc_words: "Short Description Word Limit",
    long_desc_words: "Long Description Word Limit",
    keywords: "Keywords",
  };

  const fieldNotes = {
    temperature: "Allowed values: 0.0 – 1.0",
    top_p: "Allowed values: 0.0 – 1.0",
    max_tokens: "Positive integers (e.g., 800)",
    short_desc_words: "Suggested: 25 to 200",
    long_desc_words: "Suggested: 25 to 200",
    keywords: "Comma-separated words",
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    const finalData = {
      ...form,
      keywords: form.keywords
        ? String(form.keywords).split(',').map(k => k.trim()).filter(Boolean)
        : [],
    };
    onSave(finalData);
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-box">
        <h3>Optional Settings</h3>

        {Object.keys(tooltips).map((field) => (
          <div className="modal-input" key={field}>
            <label className="field-label">
              {fieldLabels[field]}
              <div className="info-wrapper">
                <span className="info-icon">ⓘ</span>
                <div className="tooltip">{tooltips[field]}</div>
              </div>
            </label>

            <input
              type="text"
              name={field}
              value={form[field]}
              onChange={handleChange}
              placeholder={field === "tone" ? "Write professionally and highlight key features" : ""}
            />

            {field !== "tone" && fieldNotes[field] && (
              <small className="field-note">{fieldNotes[field]}</small>
            )}
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
