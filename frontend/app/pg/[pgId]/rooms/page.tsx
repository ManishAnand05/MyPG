'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { RoomApi } from '../../../../lib/api';
import { useParams } from 'next/navigation';

export default function RoomsPage() {
  const params = useParams();
  const pgId = Number(params.pgId);
  const [rooms, setRooms] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const data = await RoomApi.list(pgId);
        setRooms(data);
      } catch {
        setRooms([]);
      } finally {
        setLoading(false);
      }
    };
    fetchRooms();
  }, [pgId]);
  return (
    <div>
      <div className="card" style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <h2>Rooms for PG {pgId}</h2>
        <Link className="button" href={`/pg/${pgId}/rooms/create`}>Add Room</Link>
      </div>
      {loading ? (
        <div className="card" style={{textAlign: 'center', padding: 60}}>
          <div style={{fontSize: 48, marginBottom: 16}}>🚪</div>
          <p style={{fontSize: 16, color: '#718096'}}>Loading rooms...</p>
        </div>
      ) : (
        <div className="grid">
          {rooms.map(room => {
            const hasOccupiedBeds = room.beds?.some((bed: any) => bed.is_occupied);
            return (
              <div key={room.id} className="card">
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 12}}>
                  <h3 style={{margin: 0}}>Room #{room.room_number}</h3>
                  <button
                    onClick={async () => {
                      if (window.confirm(`Delete Room #${room.room_number}?`)) {
                        try {
                          await RoomApi.delete(room.id);
                          setRooms(rooms.filter(r => r.id !== room.id));
                        } catch (err: any) {
                          alert(err.message || 'Failed to delete room');
                        }
                      }
                    }}
                    disabled={hasOccupiedBeds}
                    title={hasOccupiedBeds ? "Cannot delete: occupied beds exist" : "Delete room"}
                    style={{
                      background: hasOccupiedBeds ? '#d1d5db' : '#ef4444',
                      color: '#fff',
                      border: 'none',
                      padding: '6px 12px',
                      borderRadius: '6px',
                      cursor: hasOccupiedBeds ? 'not-allowed' : 'pointer',
                      fontSize: 12,
                      fontWeight: 600
                    }}
                  >
                    🗑️
                  </button>
                </div>
                <div style={{display:'flex', gap:8}}>
                  <Link className="button secondary" href={`/rooms/${room.id}/beds`}>Beds</Link>
                </div>
              </div>
            );
          })}
          {rooms.length === 0 && <div className="card">No rooms yet.</div>}
        </div>
      )}
    </div>
  );
}