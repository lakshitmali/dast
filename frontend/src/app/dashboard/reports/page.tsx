// DAST Platform — Reports Page

'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { SEVERITY_CONFIG } from '@/lib/constants';

interface ReportEntry {
  scan_id: string;
  target_url: string;
  target_domain: string;
  completed_at: string | null;
  total_vulnerabilities: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  info_count: number;
}

export default function ReportsPage() {
  const [reports, setReports] = useState<ReportEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState<string | null>(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const data = await api.listReports() as ReportEntry[];
        setReports(data);
      } catch (e) { console.error(e); }
      finally { setLoading(false); }
    };
    fetchReports();
  }, []);

  const handleDownload = async (scanId: string, domain: string) => {
    setDownloading(scanId);
    try {
      const blob = await api.downloadReport(scanId);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `DAST_Report_${domain}_${new Date().toISOString().split('T')[0]}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) { console.error(e); }
    finally { setDownloading(null); }
  };

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 4 }}>
          <span className="text-gradient">Reports</span>
        </h1>
        <p style={{ color: '#94a3b8', fontSize: 14 }}>Download executive summary PDF reports for completed scans</p>
      </div>

      {loading ? (
        <div style={{ display: 'grid', gap: 16 }}>
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="skeleton" style={{ height: 120 }} />
          ))}
        </div>
      ) : reports.length === 0 ? (
        <div className="glass-card" style={{ padding: 60, textAlign: 'center' }}>
          <div style={{ fontSize: 40, marginBottom: 16 }}>◧</div>
          <h2 style={{ fontSize: 18, fontWeight: 600, color: '#f1f5f9', marginBottom: 8 }}>No Reports Available</h2>
          <p style={{ color: '#64748b', fontSize: 14 }}>
            Complete a scan to generate a downloadable PDF report
          </p>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: 16 }}>
          {reports.map(report => {
            const riskLevel = report.critical_count > 0 ? 'Critical' :
              report.high_count > 0 ? 'High' :
              report.medium_count > 0 ? 'Medium' : 'Low';
            const riskColor = report.critical_count > 0 ? SEVERITY_CONFIG.critical.color :
              report.high_count > 0 ? SEVERITY_CONFIG.high.color :
              report.medium_count > 0 ? SEVERITY_CONFIG.medium.color : SEVERITY_CONFIG.low.color;

            return (
              <div key={report.scan_id} className="glass-card" style={{
                padding: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
                    <span style={{ fontSize: 24 }}>◧</span>
                    <div>
                      <h3 style={{ fontSize: 16, fontWeight: 600, color: '#f1f5f9' }}>
                        {report.target_domain}
                      </h3>
                      <p style={{ fontSize: 12, color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                        {report.target_url}
                      </p>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: 16, marginTop: 12 }}>
                    <span style={{ fontSize: 12, color: '#94a3b8' }}>
                      <strong>{report.total_vulnerabilities}</strong> findings
                    </span>
                    <span style={{ fontSize: 12, color: SEVERITY_CONFIG.critical.color }}>
                      <strong>{report.critical_count}</strong> critical
                    </span>
                    <span style={{ fontSize: 12, color: SEVERITY_CONFIG.high.color }}>
                      <strong>{report.high_count}</strong> high
                    </span>
                    <span style={{ fontSize: 12, color: SEVERITY_CONFIG.medium.color }}>
                      <strong>{report.medium_count}</strong> medium
                    </span>
                    <span style={{ fontSize: 12, color: '#64748b' }}>
                      {report.completed_at ? new Date(report.completed_at).toLocaleDateString() : ''}
                    </span>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 11, textTransform: 'uppercase', color: '#64748b', fontWeight: 600, marginBottom: 4 }}>
                      Risk
                    </div>
                    <span style={{
                      fontSize: 12, fontWeight: 700, color: riskColor,
                      background: `${riskColor}15`, padding: '4px 12px',
                      borderRadius: 9999, border: `1px solid ${riskColor}30`,
                    }}>
                      {riskLevel}
                    </span>
                  </div>
                  <button
                    id={`download-report-${report.scan_id}`}
                    className="btn-glow btn-glow-green"
                    onClick={() => handleDownload(report.scan_id, report.target_domain)}
                    disabled={downloading === report.scan_id}
                    style={{ padding: '10px 20px', fontSize: 13 }}
                  >
                    {downloading === report.scan_id ? 'Generating...' : '↓ Download PDF'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
