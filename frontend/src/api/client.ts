// Typed fetch client. The backend speaks snake_case; we map to camelCase here at
// the boundary so the rest of the app only ever sees camelCase (see frontend/CLAUDE.md).

export interface Post {
  id: string;
  imageUrl: string;
  caption: string;
  author: string;
  createdAt: string;
  likeCount: number;
  commentCount: number;
}

export interface LikeCount {
  postId: string;
  likes: number;
}

// Shape of a post exactly as the API returns it (snake_case).
interface PostDto {
  id: string;
  image_url: string;
  caption: string;
  author: string;
  created_at: string;
  like_count: number;
  comment_count: number;
}

interface LikeCountDto {
  post_id: string;
  likes: number;
}

interface ApiError {
  detail: string;
}

function toPost(dto: PostDto): Post {
  return {
    id: dto.id,
    imageUrl: dto.image_url,
    caption: dto.caption,
    author: dto.author,
    createdAt: dto.created_at,
    likeCount: dto.like_count,
    commentCount: dto.comment_count,
  };
}

function toLikeCount(dto: LikeCountDto): LikeCount {
  return { postId: dto.post_id, likes: dto.likes };
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = (await response.json()) as ApiError;
      if (body.detail) {
        detail = body.detail;
      }
    } catch {
      // Non-JSON error body; keep the generic message.
    }
    throw new Error(detail);
  }

  return (await response.json()) as T;
}

export async function fetchFeed(limit = 20): Promise<Post[]> {
  const dtos = await request<PostDto[]>(`/posts?limit=${limit}`);
  return dtos.map(toPost);
}

export async function likePost(postId: string, user: string): Promise<LikeCount> {
  const dto = await request<LikeCountDto>(`/posts/${postId}/likes`, {
    method: 'POST',
    body: JSON.stringify({ user }),
  });
  return toLikeCount(dto);
}
