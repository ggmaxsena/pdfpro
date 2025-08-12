// frontend/app/diarias/[id]/page.js
'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import TravelRequestForm from '../components/TravelRequestForm';
import { useGetTravelRequest } from '../hooks/useDiariasApi';

export default function EditDiariaPage() {
  const params = useParams();
  const { id } = params;
  const { travelRequest, isLoading, isError } = useGetTravelRequest(id);

  if (isLoading) return <div className="text-center p-4">Carregando...</div>;
  if (isError) return <div className="text-center p-4 text-red-500">Erro ao carregar a solicitação.</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Editar Solicitação de Diária</h1>
      <TravelRequestForm initialData={travelRequest} />
    </div>
  );
}
