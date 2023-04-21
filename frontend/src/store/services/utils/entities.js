export function findEntityIndexById(entities, entityId) {
  return entities.value.findIndex((entity) => entity.id === entityId);
}
