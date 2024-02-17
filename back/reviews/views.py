from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ReviewSerializer, CommentSerializer
from .models import Review, Comment


# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def review_list(request):
#     if request.method == 'GET':
#         reviews = get_list_or_404(Review)
#         serializer = ReviewListSerializer(reviews, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             # serializer.save()
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_create(request):
    if request.method == 'GET':
        reviews = Review.objects.all()    
        serializers = ReviewSerializer(reviews, many=True)  
        return Response(serializers.data)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
   
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if request.user != review.user:
            return Response(
                {'message': '게시글은 작성자만 수정/삭제할 수 있습니다.'},
                status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if request.user != review.user:
            return Response(
               {'message': '게시글은 작성자만 삭제할 수 있습니다.'},
               status=status.HTTP_400_BAD_REQUEST
           )

        
        review.delete()
        data = {
            'pk': review_pk,
            'message': f'{review_pk}번 게시글은 삭제 되었습니다.'
        }
        return Response(data=data)
        
    
    
    # elif request.method == 'DELETE':
    #     if request.user != review.user:
    #         return Response(
    #             {'message': '게시글은 작성자만 삭제할 수 있습니다.'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    
    #     review.delete()
    #     data = {
    #         'pk': review_pk,
    #         'message': f'{review_pk}번 게시글은 삭제 되었습니다.'
    #     }
    #     return Response(data=data)
    
    



@api_view(['GET', 'POST'])
def comment_list(request, article_id):
    article = get_object_or_404(Review, id=article_id)

    # 게시글의 댓글 목록 보기 (READ)
    if request.method == 'GET':
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # 게시글에 새 댓글 작성하기 (CREATE)
    else:
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article, comment_user=request.user, username=request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def comment_update_or_delete(request, article_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.comment_user:
        return Response(
            {'message': '댓글은 작성자만 수정/삭제할 수 있습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 댓글 수정하기 (UPDATE)
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 댓글 삭제하기 (DELETE)
    else:
        comment.delete()
        return Response(
            {'message': '댓글이 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )



@api_view(['POST'])
def article_like(request, article_id):
    
    review = get_object_or_404(Review, pk=article_id)
    user = request.user
    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    else:
        review.like_users.add(user)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)