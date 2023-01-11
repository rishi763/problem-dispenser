from utils import problem_dict

def repost(args, author):
    id=author.id
    problem=problem_dict.get(id)
    if problem is None:
        return [{"text":"You are not doing a problem at this moment."}]
    return [{"file":problem.get_image()}]