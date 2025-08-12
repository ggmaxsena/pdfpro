// frontend/app/diarias/components/TravelRequestForm.js
'use client';

import React, { useState, useEffect } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import { useCreateTravelRequest, useUpdateTravelRequest, useCalculateDiarias } from '../hooks/useDiariasApi';

export default function TravelRequestForm({ initialData = null }) {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [calculationResult, setCalculationResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const createRequest = useCreateTravelRequest();
  const updateRequest = useUpdateTravelRequest();
  const calculateDiarias = useCalculateDiarias();

  const { register, handleSubmit, control, watch, reset, formState: { errors } } = useForm({
    defaultValues: initialData || {
      unidade_orcamentaria: '',
      orgao_solicitante: '',
      justificativa: '',
      objetivo: '',
      itinerario: '',
      data_ida: '',
      data_retorno: '',
      transporte_tipo: 'oficial',
      transporte_meio: 'terrestre',
      descricao_veiculo: '',
      travelers: [{ nome: '', matricula: '', cargo: '', cds: '', cpf: '', banco: '', agencia: '', conta_corrente: '', tipo: 'passageiro' }]
    }
  });

  useEffect(() => {
    if (initialData) {
      reset(initialData);
    }
  }, [initialData, reset]);

  const { fields, append, remove } = useFieldArray({
    control,
    name: "travelers"
  });

  const processSubmit = async (data) => {
    setIsSubmitting(true);
    try {
      if (initialData) {
        await updateRequest(initialData.id, data);
        alert('Solicitação atualizada com sucesso!');
      } else {
        await createRequest(data);
        alert('Solicitação criada com sucesso!');
      }
      router.push('/diarias');
    } catch (error) {
      alert(`Erro ao salvar a solicitação: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNextStep = () => setStep(s => s + 1);
  const handlePrevStep = () => setStep(s => s - 1);

  const renderStep1 = () => (
    <div>
      <h3 className="text-lg font-semibold mb-4">Informações da Viagem</h3>
      {/* Fields for Travel Request */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Unidade Orçamentária</label>
          <input {...register('unidade_orcamentaria', { required: true })} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
        </div>
        {/* Add other fields similarly */}
      </div>
      <div className="flex justify-end mt-6">
        <button type="button" onClick={handleNextStep} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Próximo
        </button>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div>
      <h3 className="text-lg font-semibold mb-4">Participantes</h3>
      {fields.map((field, index) => (
        <div key={field.id} className="p-4 border rounded-md mb-4">
          <h4 className="font-semibold">Participante {index + 1}</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
            <div>
              <label className="block text-sm font-medium text-gray-700">Nome</label>
              <input {...register(`travelers.${index}.nome`, { required: true })} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" />
            </div>
            {/* Add other traveler fields */}
          </div>
          <button type="button" onClick={() => remove(index)} className="mt-2 text-red-500 hover:underline">Remover</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ nome: '', matricula: '', cargo: '', cds: '', cpf: '', banco: '', agencia: '', conta_corrente: '', tipo: 'passageiro' })} className="text-blue-500 hover:underline">Adicionar Participante</button>
      <div className="flex justify-between mt-6">
        <button type="button" onClick={handlePrevStep} className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
          Anterior
        </button>
        <button type="submit" disabled={isSubmitting} className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
          {isSubmitting ? 'Salvando...' : (initialData ? 'Atualizar' : 'Salvar')}
        </button>
      </div>
    </div>
  );

  return (
    <form onSubmit={handleSubmit(processSubmit)} className="bg-white p-6 rounded-lg shadow-md">
      <div className="mb-4">
        <nav className="flex space-x-4">
          <button type="button" onClick={() => setStep(1)} className={`font-medium ${step === 1 ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}>Passo 1: Detalhes</button>
          <button type="button" onClick={() => setStep(2)} className={`font-medium ${step === 2 ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}>Passo 2: Participantes</button>
        </nav>
      </div>

      {step === 1 && renderStep1()}
      {step === 2 && renderStep2()}
    </form>
  );
}
