# frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
# copie package.json e yarn.lock do contexto de build (./frontend)
COPY package.json yarn.lock ./
RUN yarn install

# copie todo o código da aplicação
COPY . .

# constrói o projeto Next.js para produção
RUN yarn build

# estágio de produção
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/yarn.lock ./yarn.lock
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["yarn", "start"]