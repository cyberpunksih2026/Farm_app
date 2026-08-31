import apiClient from './axios';

const getBaseUrl = () => import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const reportApi = {
  getAttendanceReport: async (params) => {
    const res = await apiClient.get('/reports/attendance', { params });
    return res.data;
  },
  getExportCsvUrl: (params) => {
    const query = new URLSearchParams(params).toString();
    return `${getBaseUrl()}/reports/export-csv?${query}`;
  },
  getExportExcelUrl: (params) => {
    const query = new URLSearchParams(params).toString();
    return `${getBaseUrl()}/reports/export-excel?${query}`;
  },
  getExportJsonUrl: (params) => {
    const query = new URLSearchParams(params).toString();
    return `${getBaseUrl()}/reports/export-json?${query}`;
  },
  getExportHtmlUrl: (params) => {
    const query = new URLSearchParams(params).toString();
    return `${getBaseUrl()}/reports/export-html?${query}`;
  },
  // Direct client-side file downloader with JWT authentication and fallback error handling
  downloadReport: async (format, params) => {
    const endpoints = {
      excel: '/reports/export-excel',
      csv: '/reports/export-csv',
      json: '/reports/export-json',
      html: '/reports/export-html',
    };
    const endpoint = endpoints[format] || endpoints.excel;

    try {
      const res = await apiClient.get(endpoint, {
        params,
        responseType: 'blob',
      });

      const extensions = {
        excel: 'xlsx',
        csv: 'csv',
        json: 'json',
        html: 'html',
      };
      const mimeTypes = {
        excel: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        csv: 'text/csv',
        json: 'application/json',
        html: 'text/html',
      };

      const blob = new Blob([res.data], {
        type: mimeTypes[format] || 'application/octet-stream',
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const disposition = res.headers['content-disposition'] || '';
      const filenameMatch = disposition.match(/filename\*?=(?:UTF-8''|"?)([^";]+)/i);
      const start = params.start_date || 'report';
      const end = params.end_date || 'report';
      link.download = filenameMatch?.[1] || `attendance_statement_${start}_to_${end}.${extensions[format] || 'dat'}`;
      if (format === 'html') {
        link.target = '_blank';
        link.rel = 'noopener';
      }
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setTimeout(() => window.URL.revokeObjectURL(url), 1000);
    } catch (err) {
      if (err.response && err.response.data instanceof Blob) {
        const errText = await err.response.data.text();
        try {
          const errJson = JSON.parse(errText);
          err.message = errJson.detail || errJson.message || 'Export generation failed';
        } catch (e) {
          if (e === err) throw e;
          err.message = errText || 'Export generation failed';
        }
      }
      throw err;
    }
  },
};
