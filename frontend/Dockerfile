# builder -------------------------------------------------------
FROM node:20-alpine AS builder
WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install
COPY frontend/ .
RUN yarn build

# runtime -------------------------------------------------------
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
ENV PATH /app/node_modules/.bin:$PATH
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/yarn.lock ./yarn.lock
EXPOSE 3000
CMD ["yarn", "start"]