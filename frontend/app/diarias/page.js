// frontend/app/diarias/page.js
'use client';

import React from 'react';
import TravelRequestDashboard from './components/TravelRequestDashboard';

export default function DiariasPage() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Painel de Solicitação de Diárias</h1>
      <TravelRequestDashboard />
    </div>
  );
}
