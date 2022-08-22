from typing import Iterable, Callable
import bpy
import re


def flatten(list_of_lists: list[list[any]]) -> list[any]:
    """Flatten a list of lists"""
    return [item for sublist in list_of_lists for item in sublist]


def wordwrap(string: str, length: int) -> list[str]:
    """Word wrap a string to the given length"""
    words = [word for word in re.split(' +', string) if word]
    if not words: return []
    lines = [f"{words[0]} "]
    if len(words) > 1:
        for word in words[1:]:
            if len(lines[-1]) + len(word) > length:
                lines.append(f"{word} ")
                continue
            lines[-1] += f"{word} "
    lines = [line[:-1] for line in lines]
    return lines


def get_collection_of_object(obj: bpy.types.Object, default_to_context: bool = True) -> bpy.types.Collection | None:
    """Get the enclosing collection of an Object (caveat: if the object is not in the active scene, this may break)"""

    # If there's only one, return that...
    candidates = [c for c in obj.users_collection]

    if len(candidates) == 0:
        return bpy.context.scene.collection if default_to_context else None

    if len(candidates) == 1:
        return candidates[0]

    # If there are more than one, but one isn't in the current Scene
    # (e.g., it's a RigidBodyWorld), return the first that isn't...
    scene_collections = [bpy.context.scene.collection] + list(bpy.context.scene.collection.children_recursive)
    candidates = [c for c in candidates if c in scene_collections]
    if len(candidates) > 0:
        return candidates[0]

    # Return the first collection from anywhere
    return obj.users_collection[0]


def get_operator_defaults(operator_instance) -> dict[str, any]:
    """Scan annotations on the given instance and all parent classes to find default operator values"""
    defaults = {}
    for cls in [type(operator_instance)] + list(type(operator_instance).__mro__):
        for note_name, note in getattr(cls, '__annotations__', {}).items():
            if hasattr(note, "keywords") and "default" in note.keywords:
                defaults[note_name] = note.keywords["default"]
    return defaults


def reset_operator_defaults(operator_instance, keys: Iterable[str]) -> None:
    """Reset some of an operator's properties to their defaults"""
    defaults = get_operator_defaults(operator_instance)
    for key in keys:
        if key in defaults:
            setattr(operator_instance, key, defaults[key])


def uilist_sort(items: list[any], make_sortable_fn: Callable[[any], any] = lambda value: value) -> list[int]:
    """Given an unsorted list and a normalizing function, generates a list of movement directives in the form that
    UIList sorting requires."""

    # Return a list (of the same length) with the values being what index the value at that index should be moved to.
    # So, if what is index 4 should be at index 2, the array should have 2 at its index 4

    moves = [0] * len(items)

    # Achieve this by enumerating the original list, sorting the enumeration by value, then enumerating that, so
    # we have both the original position and the new (desired) one...
    for (new_index, (original_index, _)) in enumerate(sorted(enumerate(items), key=lambda item: make_sortable_fn(item[1]))):
        # ...then assigning value new_index to list item original_index
        moves[original_index] = new_index

    return moves
