import { useFeed } from '../api/hooks';
import PostCard from '../components/PostCard';

export default function Feed(): JSX.Element {
  const { data: posts, isLoading, isError, error } = useFeed();

  if (isLoading) {
    return <p className="py-10 text-center text-sm text-gray-500">Loading feed…</p>;
  }

  if (isError) {
    return (
      <p className="py-10 text-center text-sm text-rose-600">
        Could not load the feed: {error.message}
      </p>
    );
  }

  if (!posts || posts.length === 0) {
    return (
      <p className="py-10 text-center text-sm text-gray-500">
        No posts yet. Seed some with <code>python -m app.seed --demo</code>.
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
