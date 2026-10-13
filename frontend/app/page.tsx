async function getMessage() {
  const response = await fetch(
    `${process.env.BACKEND_URL}/api/hello`,
    {
      headers: {
        Authorization: `Bearer ${process.env.BACKEND_API_TOKEN}`,
      },
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch backend");
  }

  return response.json();
}

export default async function Home() {
  const data = await getMessage();

  return (
    <main>
      <h1>Next.js + Flask</h1>
      <p>{data.message}</p>
    </main>
  );
}