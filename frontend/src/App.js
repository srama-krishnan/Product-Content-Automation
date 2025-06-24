import React, { useState } from 'react';
import './styles/app.css';
import InputForm from './components/InputForm';
import SettingsModal from './components/SettingsModal';
import ResBox from './components/ResBox';
import Loader from './components/Loader';
import { generateProductContent } from './api';

function App() {
  const [formData, setFormData] = useState(null);         // {product_name, brand, sku}
  const [settings, setSettings] = useState({});            // optional config
  const [outputData, setOutputData] = useState(null);      // API response JSON
  const [loading, setLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const handleGenerate = async (mandatoryFields) => {
    setFormData(mandatoryFields);
    setLoading(true);
    setOutputData(null);

    try {
      const response = await generateProductContent({
        ...mandatoryFields,
        ...settings,
      });
      setOutputData(response);
    } catch (error) {
      console.error('Error generating content:', error);
      alert('Failed to generate content. Please check server or input.');
    } finally {
      setLoading(false);
    }
  };

  const handleSettingsSave = (updatedSettings) => {
    setSettings(updatedSettings);
    setShowSettings(false);
  };

  const handleRegenerate = () => {
    if (formData) handleGenerate(formData);
  };

  return (
    <div className="app-container">
      <h2>Product Content Generator</h2>

      <InputForm
        onGenerate={handleGenerate}
        onOpenSettings={() => setShowSettings(true)}
        isLoading={loading}
      />

      {loading && <Loader />}

      {outputData && (
        <ResBox
          data={outputData}
          onRegenerate={handleRegenerate}
          isLoading={loading}
        />
      )}

      {showSettings && (
        <SettingsModal
          initialValues={settings}
          onClose={() => setShowSettings(false)}
          onSave={handleSettingsSave}
        />
      )}
    </div>
  );
}

export default App;
