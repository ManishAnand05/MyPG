'use client';
import { useState } from 'react';
import { BedApi } from '../../../../../lib/api';
import { useParams, useRouter } from 'next/navigation';

export default function BedCreatePage() {
  const params = useParams();
  const roomId = Number(params?.roomId);
  const [rent, setRent] = useState<string>('');
  const [validationError, setValidationError] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleRentChange = (value: string) => {
    setRent(value);
    if (value && !/^\d+$/.test(value)) {
      setValidationError('Rent must be a positive integer');
    } else {
      setValidationError(null);
    }
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    
    if (!rent || !/^\d+$/.test(rent)) {
      setValidationError('Rent must be a positive integer');
      return;
    }

    try {
      await BedApi.create(roomId, Number(rent));
      router.push(`/rooms/${roomId}/beds`);
    } catch (err: any) {
      setError(err.message || 'Create failed');
    }
  };

  return (
    <div className="card" style={{maxWidth: 500}}>
      <h2>Add Bed</h2>
      <form className="form" onSubmit={onSubmit}>
        <div>
          <label className="form-label">Monthly Rent (₹)</label>
          <input className="input" type="text" placeholder="e.g., 5000, 10000" value={rent} onChange={e => handleRentChange(e.target.value)} required />
          {validationError && <div style={{color:'crimson', fontSize: 13, marginTop: 6}}>{validationError}</div>}
        </div>
        {error && <div style={{color:'crimson', marginBottom: 16}}>{error}</div>}
        <button className="button" type="submit" style={{width: '100%'}} disabled={!!validationError || !rent}>Create Bed</button>
      </form>
    </div>
  );
}