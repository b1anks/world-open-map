const API_URL = import.meta.env.VITE_API_URL || '';

export async function getOverview() {
  const response = await fetch(`${API_URL}/api/overview`);
  return response.json();
}

export async function getMapBounds() {
  const response = await fetch(`${API_URL}/api/map/bounds`);
  return response.json();
}
