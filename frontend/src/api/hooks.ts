// TanStack Query hooks. Server state lives here; components never call fetch directly.
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { fetchFeed, likePost, type LikeCount, type Post } from './client';

const FEED_KEY = ['feed'] as const;

export function useFeed() {
  return useQuery<Post[], Error>({
    queryKey: FEED_KEY,
    queryFn: () => fetchFeed(),
  });
}

interface LikeVariables {
  postId: string;
  user: string;
}

export function useLikePost() {
  const queryClient = useQueryClient();

  return useMutation<LikeCount, Error, LikeVariables>({
    mutationFn: ({ postId, user }) => likePost(postId, user),
    onSuccess: (result) => {
      // Reflect the authoritative count from the server in the cached feed.
      queryClient.setQueryData<Post[]>(FEED_KEY, (posts) =>
        posts?.map((post) =>
          post.id === result.postId ? { ...post, likeCount: result.likes } : post,
        ),
      );
    },
  });
}
