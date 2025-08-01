"use client";

import UploadButton from "../../../components/UploadButton";

export default function AnonimizarNome() {
  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-bold">Anonimizar apenas o Nome</h1>
      <UploadButton
        endpoint="/api/excel/anonymize/name/"
        label="Anonimizar Nome"
        accept=".xlsx"
      />
    </main>
  );
}
