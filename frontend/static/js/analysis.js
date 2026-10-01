document.addEventListener('DOMContentLoaded', async () => {
  const select = document.getElementById('analysis-symbol');
  if (!select) return;

  const statusNode = document.getElementById('analysis-state');
  const runButton = document.getElementById('run-analysis');
  const exportButton = document.getElementById('export-analysis');
  const refreshButton = document.getElementById('refresh-market-data');
  let latestReport;

  const setText = (id, value) => {
    const node = document.getElementById(id);
    if (node) node.textContent = value;
  };
  const finite = (value) => value !== null && value !== undefined && Number.isFinite(Number(value));
  const fixed = (value, digits = 2) => finite(value) ? Number(value).toFixed(digits) : 'N/A';
  const percent = (value) => `${fixed(value)}%`;
  const money = (value) => `$${Number(value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

  const fetchJson = async (url) => {
    const response = await fetch(url);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || `Request failed (${response.status})`);
    return payload;
  };

  const loadDataStatus = async () => {
    const status = await fetchJson('/api/v1/market-data/status');
    const dataset = status.datasets.find((item) => item.symbol === select.value);
    if (!dataset) {
      setText('data-freshness', 'No local dataset for selected symbol');
      setText('data-provider', 'Provider: unavailable');
      setText('data-validation', 'Validation: unavailable');
      return;
    }
    const age = dataset.age_calendar_days === null || dataset.age_calendar_days === undefined
      ? 'age unknown'
      : `${dataset.age_calendar_days} calendar days since last bar`;
    const freshnessNode = document.getElementById('data-freshness');
    freshnessNode.textContent = `${dataset.symbol}: ${dataset.end_date || 'no end date'} / ${age}`;
    freshnessNode.classList.toggle('is-stale', dataset.age_calendar_days > 7);
    setText('data-provider', `Provider: ${dataset.provider}${dataset.retrieved_at_utc ? ` / retrieved ${new Date(dataset.retrieved_at_utc).toLocaleString()}` : ' / retrieval not recorded'}`);
    setText('data-validation', `Validation: ${dataset.validation}${dataset.warnings?.length ? ` / ${dataset.warnings.length} warning(s)` : ''}`);
    document.getElementById('data-validation').classList.toggle('is-error', dataset.validation !== 'passed');
  };

  const loadReport = async () => {
    if (!select.value) return;
    const strategy = document.getElementById('analysis-strategy').value;
    runButton.disabled = true;
    statusNode.classList.remove('is-error');
    statusNode.textContent = `Computing historical analysis for ${select.value}...`;
    try {
      const query = new URLSearchParams({ symbol: select.value, strategy });
      latestReport = await fetchJson(`/api/v1/analysis/report?${query}`);
      renderReport(latestReport);
      statusNode.textContent = `Analysis complete: ${latestReport.dataset.symbol} / ${latestReport.dataset.rows.toLocaleString()} observations`;
      exportButton.disabled = false;
      await loadDataStatus();
    } catch (error) {
      statusNode.textContent = error.message;
      statusNode.classList.add('is-error');
      exportButton.disabled = true;
    } finally {
      runButton.disabled = false;
    }
  };

  const renderReport = (report) => {
    const market = report.market;
    setText('dataset-description', `${report.dataset.symbol} / ${report.dataset.rows.toLocaleString()} rows / ${report.dataset.source}`);
    setText('analysis-source', report.data_status.replaceAll('_', ' '));
    setText('market-total-return', percent(market.total_return_pct));
    setText('market-volatility', percent(market.annualized_volatility_pct));
    setText('market-sharpe', fixed(market.sharpe_ratio));
    setText('market-drawdown', percent(market.max_drawdown_pct));
    setText('market-date-range', `${report.dataset.start_date} to ${report.dataset.end_date}`);

    const technical = report.technical;
    setText('technical-date', report.dataset.end_date);
    setText('technical-close', money(technical.close));
    setText('technical-sma-20', money(technical.sma_20));
    setText('technical-sma-50', money(technical.sma_50));
    setText('technical-rsi', fixed(technical.rsi));
    setText('technical-macd', `${fixed(technical.macd, 3)} / ${fixed(technical.macd_signal, 3)}`);
    setText('technical-atr', money(technical.atr));
    setText('technical-daily-return', percent(Number(technical.daily_return) * 100));

    renderStrategyTable(report.strategies);
    renderChart(report.strategies);
    renderPortfolio(report.portfolio);
    renderTailRisk(report.risk);
    renderCorrelation(report.portfolio.correlation);
    renderMonteCarlo(report.monte_carlo);
    setText('analysis-assumptions', `${report.assumptions.signal_timing} Costs: ${fixed(report.assumptions.transaction_cost_pct_per_turnover, 3)}% per position turnover. ${report.assumptions.not_included}`);
  };

  const renderStrategyTable = (strategies) => {
    const body = document.getElementById('strategy-results');
    body.replaceChildren(...strategies.map((strategy) => {
      const row = document.createElement('tr');
      const values = [
        strategy.name,
        percent(strategy.total_return_pct),
        percent(strategy.annualized_volatility_pct),
        fixed(strategy.sharpe_ratio),
        percent(strategy.max_drawdown_pct),
        String(strategy.trade_entries),
      ];
      values.forEach((value) => {
        const cell = document.createElement('td');
        cell.textContent = value;
        row.appendChild(cell);
      });
      return row;
    }));
  };

  const renderPortfolio = (portfolio) => {
    setText('portfolio-symbol-count', `${portfolio.symbols.length} symbols`);
    setText('portfolio-return', percent(portfolio.equal_weight.annualized_return_pct));
    setText('portfolio-volatility', percent(portfolio.equal_weight.annualized_volatility_pct));
    setText('portfolio-sharpe', fixed(portfolio.equal_weight.sharpe_ratio));
  };

  const renderTailRisk = (risk) => {
    setText('risk-var', percent(risk.var_95_daily_pct));
    setText('risk-cvar', percent(risk.cvar_95_daily_pct));
  };

  const renderMonteCarlo = (monteCarlo) => {
    setText('mc-probability-loss', percent(monteCarlo.probability_of_loss_pct));
    setText('mc-p5', percent(monteCarlo.p5_return_pct));
    setText('mc-median', percent(monteCarlo.median_return_pct));
    setText('mc-p95', percent(monteCarlo.p95_return_pct));
    setText('mc-method', `${latestReport.monte_carlo_strategy}: ${monteCarlo.simulations.toLocaleString()} deterministic-seed simulations, ${monteCarlo.horizon_trading_days} trading days each.`);
  };

  const renderCorrelation = (matrix) => {
    const table = document.getElementById('correlation-matrix');
    const symbols = Object.keys(matrix);
    const head = document.createElement('thead');
    const header = document.createElement('tr');
    const corner = document.createElement('th');
    corner.scope = 'col';
    corner.textContent = 'Asset';
    header.appendChild(corner);
    symbols.forEach((symbol) => {
      const cell = document.createElement('th');
      cell.scope = 'col';
      cell.textContent = symbol;
      header.appendChild(cell);
    });
    head.appendChild(header);

    const body = document.createElement('tbody');
    symbols.forEach((rowSymbol) => {
      const row = document.createElement('tr');
      const label = document.createElement('th');
      label.scope = 'row';
      label.textContent = rowSymbol;
      row.appendChild(label);
      symbols.forEach((columnSymbol) => {
        const value = matrix[rowSymbol][columnSymbol];
        const cell = document.createElement('td');
        cell.textContent = fixed(value, 2);
        const strength = Math.min(0.16, Math.abs(Number(value)) * 0.16);
        cell.style.backgroundColor = Number(value) < 0
          ? `rgba(248, 113, 113, ${strength})`
          : `rgba(34, 197, 94, ${strength})`;
        cell.title = `${rowSymbol} / ${columnSymbol}: ${fixed(value, 3)}`;
        row.appendChild(cell);
      });
      body.appendChild(row);
    });
    table.replaceChildren(head, body);
  };

  const renderChart = (strategies) => {
    const canvas = document.getElementById('equity-chart');
    const context = canvas.getContext('2d');
    const bounds = canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.max(1, Math.floor(bounds.width * ratio));
    canvas.height = Math.max(1, Math.floor(bounds.height * ratio));
    context.scale(ratio, ratio);
    const width = bounds.width;
    const height = bounds.height;
    const pad = { left: 48, right: 12, top: 12, bottom: 26 };
    const plotWidth = width - pad.left - pad.right;
    const plotHeight = height - pad.top - pad.bottom;
    const colors = ['#84cc16', '#60a5fa', '#fbbf24'];
    const values = strategies.flatMap((strategy) => strategy.equity_curve.map((point) => point.value));
    if (!values.length) return;
    let minValue = Math.min(...values);
    let maxValue = Math.max(...values);
    if (minValue === maxValue) maxValue = minValue + 1;
    const range = maxValue - minValue;

    context.font = '11px Inter, sans-serif';
    context.strokeStyle = 'rgba(148, 163, 184, 0.18)';
    context.fillStyle = '#9bb0c8';
    context.lineWidth = 1;
    for (let tick = 0; tick <= 4; tick += 1) {
      const y = pad.top + (plotHeight * tick / 4);
      const value = maxValue - (range * tick / 4);
      context.beginPath();
      context.moveTo(pad.left, y);
      context.lineTo(width - pad.right, y);
      context.stroke();
      context.fillText(value.toFixed(0), 4, y + 4);
    }

    strategies.forEach((strategy, index) => {
      const points = strategy.equity_curve;
      context.beginPath();
      context.strokeStyle = colors[index % colors.length];
      context.lineWidth = 2;
      points.forEach((point, pointIndex) => {
        const x = pad.left + (pointIndex / Math.max(1, points.length - 1)) * plotWidth;
        const y = pad.top + ((maxValue - point.value) / range) * plotHeight;
        if (pointIndex === 0) context.moveTo(x, y);
        else context.lineTo(x, y);
      });
      context.stroke();
    });

    const legend = document.getElementById('equity-chart-legend');
    legend.replaceChildren(...strategies.map((strategy, index) => {
      const item = document.createElement('span');
      item.className = 'legend-item';
      const swatch = document.createElement('span');
      swatch.className = 'legend-swatch';
      swatch.style.backgroundColor = colors[index % colors.length];
      item.append(swatch, document.createTextNode(strategy.name));
      return item;
    }));
  };

  document.getElementById('analysis-controls').addEventListener('submit', (event) => {
    event.preventDefault();
    loadReport();
  });
  [select, document.getElementById('analysis-strategy')].forEach((control) => {
    control.addEventListener('change', () => {
      exportButton.disabled = true;
      statusNode.textContent = 'Settings changed. Run analysis to update results.';
    });
  });
  exportButton.addEventListener('click', () => {
    if (!latestReport) return;
    const blobUrl = URL.createObjectURL(new Blob([JSON.stringify(latestReport, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = `quanttrade-analysis-${latestReport.dataset.symbol}.json`;
    link.click();
    URL.revokeObjectURL(blobUrl);
  });
  refreshButton.addEventListener('click', async () => {
    refreshButton.disabled = true;
    document.getElementById('refresh-state').classList.remove('is-error');
    setText('refresh-state', `Refreshing ${select.value} from Yahoo Finance...`);
    try {
      const response = await fetch('/api/v1/market-data/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: select.value, period: document.getElementById('refresh-period').value }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || `Refresh failed (${response.status})`);
      setText('refresh-state', `Updated ${payload.symbol}: ${payload.rows.toLocaleString()} rows, ${payload.start_date} to ${payload.end_date}. Previous raw data archived.`);
      await loadDataStatus();
      await loadReport();
    } catch (error) {
      setText('refresh-state', error.message);
      document.getElementById('refresh-state').classList.add('is-error');
    } finally {
      refreshButton.disabled = false;
    }
  });
  select.addEventListener('change', () => {
    exportButton.disabled = true;
    loadDataStatus().catch((error) => setText('data-freshness', `Status unavailable: ${error.message}`));
  });

  try {
    const catalog = await fetchJson('/api/v1/analysis/catalog');
    select.replaceChildren(...catalog.symbols.map((symbol) => {
      const option = document.createElement('option');
      option.value = symbol;
      option.textContent = symbol;
      return option;
    }));
    if (catalog.symbols.includes('AAPL')) select.value = 'AAPL';
    setText('readiness-optimization', catalog.analyses.parameter_optimization.replaceAll('_', ' '));
    setText('readiness-walk-forward', catalog.analyses.walk_forward_validation.replaceAll('_', ' '));
    setText('readiness-ml', catalog.analyses.machine_learning.replaceAll('_', ' '));
    await loadReport();
    window.addEventListener('resize', () => {
      if (latestReport) renderChart(latestReport.strategies);
    });
  } catch (error) {
    statusNode.textContent = `Dataset catalog unavailable: ${error.message}`;
    statusNode.classList.add('is-error');
  }
});
