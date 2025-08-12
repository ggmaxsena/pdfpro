// frontend/app/diarias/nova/page.js
'use client';

import React from 'react';
import TravelRequestForm from '../components/TravelRequestForm';

export default function NovaDiariaPage() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Nova Solicitação de Diária</h1>
      <TravelRequestForm />
    </div>
  );
}
