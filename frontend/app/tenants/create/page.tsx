'use client';
import { useState, useEffect } from 'react';
import { TenantApi, BedApi } from '../../../lib/api';
import { useRouter } from 'next/navigation';

type UnassignedTenant = { id: number; name: string; email: string; role: string };
type AvailableBed = { bed_id: number; rent: number; room_id: number; room_number: number; pg_id: number; pg_name: string; pg_address: string };

export default function TenantAssignPage() {
  const [unassignedTenants, setUnassignedTenants] = useState<UnassignedTenant[]>([]);
  const [availableBeds, setAvailableBeds] = useState<AvailableBed[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // For each tenant, track their selected bed and move-in date
  const [assignments, setAssignments] = useState<Record<number, { bedId: number | null; moveInDate: string }>>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [tenants, beds] = await Promise.all([
          TenantApi.unassigned(),
          BedApi.available()
        ]);
        setUnassignedTenants(tenants);
        setAvailableBeds(beds);
        
        // Initialize assignments state
        const initialAssignments: Record<number, { bedId: number | null; moveInDate: string }> = {};
        tenants.forEach(t => {
          initialAssignments[t.id] = { bedId: null, moveInDate: '' };
        });
        setAssignments(initialAssignments);
      } catch (err: any) {
        setError(err.message || 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const onAssign = async (tenantId: number) => {
    const assignment = assignments[tenantId];
    if (!assignment.bedId || !assignment.moveInDate) {
      alert('Please select a bed and move-in date');
      return;
    }

    try {
      await TenantApi.create(tenantId, assignment.bedId, assignment.moveInDate);
      // Remove from unassigned list
      setUnassignedTenants(prev => prev.filter(t => t.id !== tenantId));
      // Remove the assigned bed from available beds
      setAvailableBeds(prev => prev.filter(b => b.bed_id !== assignment.bedId));
      alert('Tenant assigned successfully!');
    } catch (err: any) {
      alert(err.message || 'Failed to assign tenant');
    }
  };

  // Group beds by PG
  const bedsByPg = availableBeds.reduce((acc, bed) => {
    if (!acc[bed.pg_id]) {
      acc[bed.pg_id] = { pg_name: bed.pg_name, pg_address: bed.pg_address, beds: [] };
    }
    acc[bed.pg_id].beds.push(bed);
    return acc;
  }, {} as Record<number, { pg_name: string; pg_address: string; beds: AvailableBed[] }>);

  if (loading) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: 60 }}>
        <div style={{ fontSize: 48, marginBottom: 16 }}>👥</div>
        <p style={{ fontSize: 16, color: '#718096' }}>Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>Assign Tenants to Beds</h2>
          <p className="subtitle">Assign new tenants to available beds in your properties</p>
        </div>
      </div>

      {error && (
        <div className="card" style={{ background: '#fee', color: 'crimson', marginBottom: 20 }}>
          {error}
        </div>
      )}

      {unassignedTenants.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: 40 }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>✓</div>
          <p style={{ fontSize: 16, color: '#718096' }}>All tenants are assigned! No pending assignments.</p>
        </div>
      ) : (
        <div className="grid-2">
          {unassignedTenants.map(tenant => (
            <div key={tenant.id} className="card">
              <div style={{ display: 'flex', alignItems: 'start', gap: 12, marginBottom: 16 }}>
                <div className="hero-icon" style={{ margin: 0, width: 40, height: 40, fontSize: 20 }}>👤</div>
                <div style={{ flex: 1 }}>
                  <h3 style={{ margin: '0 0 4px 0' }}>{tenant.name}</h3>
                  <p style={{ margin: 0, color: '#718096', fontSize: 14 }}>{tenant.email}</p>
                </div>
              </div>

              <div style={{ marginBottom: 12 }}>
                <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#4a5568', marginBottom: 6 }}>
                  Select Bed
                </label>
                <select
                  className="input"
                  value={assignments[tenant.id]?.bedId || ''}
                  onChange={e => {
                    const bedId = Number(e.target.value);
                    setAssignments(prev => ({
                      ...prev,
                      [tenant.id]: { ...prev[tenant.id], bedId: bedId || null }
                    }));
                  }}
                  style={{ width: '100%' }}
                >
                  <option value="">-- Select a bed --</option>
                  {Object.entries(bedsByPg).map(([pgId, pgData]) => (
                    <optgroup key={pgId} label={`${pgData.pg_name} - ${pgData.pg_address}`}>
                      {pgData.beds.map(bed => (
                        <option key={bed.bed_id} value={bed.bed_id}>
                          Room {bed.room_number} - Bed #{bed.bed_id} (₹{bed.rent}/mo)
                        </option>
                      ))}
                    </optgroup>
                  ))}
                </select>
              </div>

              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#4a5568', marginBottom: 6 }}>
                  Move-in Date
                </label>
                <input
                  type="date"
                  className="input"
                  value={assignments[tenant.id]?.moveInDate || ''}
                  onChange={e => {
                    setAssignments(prev => ({
                      ...prev,
                      [tenant.id]: { ...prev[tenant.id], moveInDate: e.target.value }
                    }));
                  }}
                  style={{ width: '100%' }}
                />
              </div>

              <button
                className="button"
                onClick={() => onAssign(tenant.id)}
                disabled={!assignments[tenant.id]?.bedId || !assignments[tenant.id]?.moveInDate}
                style={{
                  width: '100%',
                  opacity: (!assignments[tenant.id]?.bedId || !assignments[tenant.id]?.moveInDate) ? 0.5 : 1,
                  cursor: (!assignments[tenant.id]?.bedId || !assignments[tenant.id]?.moveInDate) ? 'not-allowed' : 'pointer'
                }}
              >
                Assign Tenant
              </button>
            </div>
          ))}
        </div>
      )}

      {availableBeds.length === 0 && unassignedTenants.length > 0 && (
        <div className="card" style={{ background: '#fffbeb', border: '1px solid #fcd34d', marginTop: 20 }}>
          <p style={{ margin: 0, color: '#92400e' }}>⚠️ No available beds. Create beds in your PGs to assign tenants.</p>
        </div>
      )}
    </div>
  );
}