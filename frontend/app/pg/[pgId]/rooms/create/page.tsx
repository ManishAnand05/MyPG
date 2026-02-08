'use client';
import { useState } from 'react';
import { RoomApi } from '../../../../../lib/api';
import { useParams, useRouter } from 'next/navigation';

export default function RoomCreatePage() {
  const params = useParams();
  const pgId = Number(params?.pgId);
  const [roomNumber, setRoomNumber] = useState<string>('');
  const [validationError, setValidationError] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleRoomNumberChange = (value: string) => {
    setRoomNumber(value);
    if (value && !/^\d+$/.test(value)) {
      setValidationError('Room number must be a positive integer');
    } else {
      setValidationError(null);
    }
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    
    if (!roomNumber || !/^\d+$/.test(roomNumber)) {
      setValidationError('Room number must be a positive integer');
      return;
    }

    try {
      await RoomApi.create(pgId, Number(roomNumber));
      router.push(`/pg/${pgId}/rooms`);
    } catch (err: any) {
      setError(err.message || 'Create failed');
    }
  };

  return (
    <div className="card" style={{maxWidth: 500}}>
      <h2>Add Room</h2>
      <form className="form" onSubmit={onSubmit}>
        <div>
          <label className="form-label">Room Number</label>
          <input className="input" type="text" placeholder="e.g., 101, 102" value={roomNumber} onChange={e => handleRoomNumberChange(e.target.value)} required />
          {validationError && <div style={{color:'crimson', fontSize: 13, marginTop: 6}}>{validationError}</div>}
        </div>
        {error && <div style={{color:'crimson', marginBottom: 16}}>{error}</div>}
        <button className="button" type="submit" style={{width: '100%'}} disabled={!!validationError || !roomNumber}>Create Room</button>
      </form>
    </div>
  );
}