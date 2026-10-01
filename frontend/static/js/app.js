document.addEventListener('DOMContentLoaded', async () => {
  const setText = (id, value) => {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
  };

  const loadCatalog = async () => {
    const response = await fetch('/api/v1/analysis/catalog');
    if (!response.ok) throw new Error(`Dataset catalog returned ${response.status}`);
    return response.json();
  };

  try {
    const catalog = await loadCatalog();
    const range = catalog.datasets.length
      ? `${catalog.datasets[0].start_date} to ${catalog.datasets[0].end_date}`
      : 'No local data';
    setText('dataset-count', String(catalog.symbols.length));
    setText('dataset-date-range', range);
    setText('operations-dataset-count', String(catalog.symbols.length));
    setText('operations-date-range', range);
    setText('data-source-status', 'Local CSV');

    Object.entries({
      'readiness-optimization': catalog.analyses.parameter_optimization,
      'readiness-walk-forward': catalog.analyses.walk_forward_validation,
      'readiness-ml': catalog.analyses.machine_learning,
    }).forEach(([id, value]) => setText(id, value.replaceAll('_', ' ')));

    const symbolSelect = document.getElementById('analysis-symbol');
    if (symbolSelect) {
      symbolSelect.replaceChildren(...catalog.symbols.map((symbol) => {
        const option = document.createElement('option');
        option.value = symbol;
        option.textContent = symbol;
        return option;
      }));
      const preferred = catalog.symbols.includes('AAPL') ? 'AAPL' : catalog.symbols[0];
      if (preferred) symbolSelect.value = preferred;
      document.dispatchEvent(new CustomEvent('analysis-catalog-ready'));
    }
  } catch (error) {
    setText('dataset-count', 'Unavailable');
    setText('dataset-date-range', 'Catalog unavailable');
    setText('operations-dataset-count', 'Unavailable');
    setText('operations-date-range', 'Catalog unavailable');
    setText('data-source-status', 'Unavailable');
    console.error('Dataset catalog unavailable:', error);
  }

  const healthNode = document.getElementById('api-health');
  if (healthNode) {
    try {
      const response = await fetch('/health');
      setText('api-health', response.ok ? 'Healthy' : 'Unavailable');
    } catch (error) {
      setText('api-health', 'Unavailable');
    }
  }
});
