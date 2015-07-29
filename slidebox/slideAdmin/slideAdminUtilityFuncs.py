import pdb

def convert_to_total_number_of_sections(animalID,slideNum,sectionNum):
    """takes a slide number and section number and converts them into the total
    number of sections for ease of calculations, using the value given to
    sectionPerSlide for the animalID as a conversion factor.

    E.g., if for animalID "gy6or6", sectionsPerSlide = 6, then when
    slide 5 section 5 is passed to convert_to_total_number_of_sections
    will return: 5 slides * 6 sections/slide + 5 sections = 35 sections total
    (counting from the first section and including section 5 on slide 5)."""
    sectionsPerSlide = animalID.sectionsPerSlide
    return slideNum * sectionsPerSlide + sectionNum


def convert_to_slide_and_section_number(animalID,abs_sectionNum):
    """takes the absolute section number (like those calculated by the
    convert_to_abs_section_number function) and converts it into the slide
    number and section number, using the sectionPerSlide value from the animalID
    model instance passed to the function.

    E.g., if for animalID "gy6or6", sectionsPerSlide = 6, then for
    abs_sectionNum = 36, the function would return:
    {'slideNum': 5
    """
    sectionsPerSlide = animalID.sectionsPerSlide
    slideNum = abs_sectionNum // sectionsPerSlide # // returns integer quotient
    sectionNum = abs_sectionNum % sectionsPerSlide # % returns remainder
    if sectionNum == 0:  # last section on a slide will return remainder of 0
        sectionNum = sectionsPerSlide # in that case, set sectionNum equal to sectionsPerSlide
    return slideNum,sectionNum
