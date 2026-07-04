import { useLikePost } from '../api/hooks';
import type { Post } from '../api/client';

// The current viewer. In a real app this would come from auth; hard-coded here so
// the like button is idempotent per-user against the backend.
const CURRENT_USER = 'demo';

interface PostCardProps {
  post: Post;
}

export default function PostCard({ post }: PostCardProps): JSX.Element {
  const likeMutation = useLikePost();

  const handleLike = (): void => {
    likeMutation.mutate({ postId: post.id, user: CURRENT_USER });
  };

  return (
    <article className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
      <header className="px-4 py-3">
        <span className="text-sm font-semibold">{post.author}</span>
      </header>

      <img
        src={post.imageUrl}
        alt={post.caption || `Post by ${post.author}`}
        className="aspect-square w-full object-cover"
      />

      <div className="px-4 py-3">
        <div className="flex items-center gap-4">
          <button
            type="button"
            onClick={handleLike}
            disabled={likeMutation.isPending}
            className="rounded-md bg-rose-50 px-3 py-1 text-sm font-medium text-rose-600 hover:bg-rose-100 disabled:opacity-50"
          >
            ♥ {post.likeCount}
          </button>
          <span className="text-sm text-gray-500">
            {post.commentCount} {post.commentCount === 1 ? 'comment' : 'comments'}
          </span>
        </div>

        {post.caption && (
          <p className="mt-2 text-sm">
            <span className="font-semibold">{post.author}</span> {post.caption}
          </p>
        )}
      </div>
    </article>
  );
}
