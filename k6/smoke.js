import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8000';
const JSON_HEADERS = { headers: { 'Content-Type': 'application/json' } };

export const options = {
  vus: 5,
  duration: '20s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<300'],
  },
};

export function setup() {
  const resposta = http.post(
    `${BASE_URL}/componentes`,
    JSON.stringify({
      nome: 'Resistor k6',
      categoria: 'resistor',
      quantidade_total: 1000000,
    }),
    JSON_HEADERS,
  );
  return { componenteId: resposta.json('id') };
}

export default function (dados) {
  const responsavel = `vu${__VU}-it${__ITER}`;

  const emprestimo = http.post(
    `${BASE_URL}/emprestimos`,
    JSON.stringify({
      componente_id: dados.componenteId,
      responsavel: responsavel,
      quantidade: 1,
    }),
    JSON_HEADERS,
  );
  check(emprestimo, { 'emprestimo criado (201)': (r) => r.status === 201 });

  const devolucao = http.post(
    `${BASE_URL}/emprestimos/${emprestimo.json('id')}/devolucao`,
  );
  check(devolucao, { 'devolucao (200)': (r) => r.status === 200 });

  const lista = http.get(`${BASE_URL}/componentes`);
  check(lista, { 'listagem (200)': (r) => r.status === 200 });
}