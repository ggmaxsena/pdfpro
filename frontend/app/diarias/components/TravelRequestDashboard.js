// frontend/app/diarias/components/TravelRequestDashboard.js
'use client';

import React from 'react';
import Link from 'next/link';
import { useGetTravelRequests, useDeleteTravelRequest } from '../hooks/useDiariasApi';

export default function TravelRequestDashboard() {
  const { travelRequests, isLoading, isError, mutate } = useGetTravelRequests();
  const deleteRequest = useDeleteTravelRequest();

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta solicitação?')) {
      try {
        await deleteRequest(id);
        mutate(); // Re-fetch the data after deletion
      } catch (error) {
        alert(`Erro ao excluir a solicitação: ${error.message}`);
      }
    }
  };

  if (isLoading) return <div className="text-center p-4">Carregando...</div>;
  if (isError) return <div className="text-center p-4 text-red-500">Erro ao carregar as solicitações.</div>;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Minhas Solicitações de Viagem</h2>
        <Link href="/diarias/nova" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Adicionar Nova
        </Link>
      </div>
      
      {travelRequests && travelRequests.length === 0 ? (
        <p>Nenhuma solicitação de viagem encontrada.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white">
            <thead className="bg-gray-200">
              <tr>
                <th className="py-2 px-4 border-b">ID</th>
                <th className="py-2 px-4 border-b">Objetivo</th>
                <th className="py-2 px-4 border-b">Período</th>
                <th className="py-2 px-4 border-b">Ações</th>
              </tr>
            </thead>
            <tbody>
              {travelRequests && travelRequests.map((request) => (
                <tr key={request.id} className="hover:bg-gray-100">
                  <td className="py-2 px-4 border-b">{request.id}</td>
                  <td className="py-2 px-4 border-b">{request.objetivo}</td>
                  <td className="py-2 px-4 border-b">{new Date(request.data_ida).toLocaleDateString()} a {new Date(request.data_retorno).toLocaleDateString()}</td>
                  <td className="py-2 px-4 border-b">
                    <Link href={`/diarias/${request.id}`} className="text-blue-500 hover:underline mr-4">Editar</Link>
                    <button onClick={() => handleDelete(request.id)} className="text-red-500 hover:underline">Excluir</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}