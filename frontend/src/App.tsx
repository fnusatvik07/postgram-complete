import Feed from './pages/Feed';

export default function App(): JSX.Element {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto max-w-xl px-4 py-4">
          <h1 className="text-xl font-semibold tracking-tight">Postgram</h1>
        </div>
      </header>
      <main className="mx-auto max-w-xl px-4 py-6">
        <Feed />
      </main>
    </div>
  );
}
