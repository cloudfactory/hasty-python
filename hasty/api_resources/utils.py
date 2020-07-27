from . import Dataset, Image, Label, LabelClass, LabelAttribute, LabelClassAttribute

class Utils:

    @staticmethod
    def copy_images(API_class_src, API_class_dst, project_id_src, project_id_dst, dataset_mapping):
        '''
        copy every image in a project to an other
        '''
        images = Image.fetch_all(API_class_src, project_id_src)
        image_mapping = {}
        for image in images:
            ret = Image.copy(API_class_dst, project_id_dst, image, dataset_mapping)
            image_mapping[image['id']] = ret['id']
        return image_mapping
        
    @staticmethod
    def copy_label_classes(API_class_src, API_class_dst, project_id_src, project_id_dst):
        '''
        copy every label class in a project to an other
        '''
        label_classes = LabelClass.fetch_all(API_class_src, project_id_src)
        label_class_mapping = {}
        for label_class in label_classes:
            ret = LabelClass.copy(API_class_dst, project_id_dst, label_class)
            label_class_mapping[label_class['id']] = ret['id']
        return label_class_mapping

    @staticmethod
    def copy_attribute_classes(API_class_src, API_class_dst, project_id_src, project_id_dst):
        '''
        copy every attribute class in a project to an other
        '''
        attribute_classes = LabelClassAttribute.fetch_all(API_class_src, project_id_src)
        attribute_class_mapping = {}
        for attribute_class in attribute_classes:
            ret = LabelClassAttribute.copy(API_class_dst, project_id_dst, attribute_class)
            attribute_class_mapping[attribute_class['id']] = ret['id']
        return attribute_class_mapping
        
    @staticmethod
    def copy_datasets(API_class_src, API_class_dst, project_id_src, project_id_dst):
        '''
        copy every dataset in a project to an other
        '''
        datasets = Dataset.fetch_all(API_class_src, project_id_src)
        dataset_mapping = {}
        for dataset in datasets:
            ret = Dataset.copy(API_class_dst, project_id_dst, dataset)
            dataset_mapping[dataset['id']] = ret['id']
        return dataset_mapping

    @staticmethod
    def copy_labels(API_class_src, API_class_dst, project_id_src, project_id_dst, image_mapping, label_class_mapping):
        '''
        copy every label in a project to an other
        '''
        labels = Label.fetch_all(API_class_src, project_id_src)
        label_mapping = {}
        for label in labels:
            ret = Label.copy(API_class_dst, project_id_dst, label, image_mapping, label_class_mapping)
            label_mapping[label['id']] = ret['id']
        return label_mapping

    #TODO: add label attributes
    def copy_labels_attribute(API_class_src, API_class_dst, project_id_src, project_id_dst):
        '''
        copy every label attribute in a project to an other
        '''
        return

    @staticmethod
    def copy_project(API_class_src, API_class_dst, project_id_src, project_id_dst):
        label_class_mapping = Utils.copy_label_classes(API_class_src, API_class_dst, project_id_src, project_id_dst)
        dataset_mapping = Utils.copy_datasets(API_class_src, API_class_dst, project_id_src, project_id_dst)
        image_mapping = Utils.copy_images(API_class_src, API_class_dst, project_id_src, project_id_dst, dataset_mapping)
        label_mapping = Utils.copy_labels(API_class_src, API_class_dst, project_id_src, project_id_dst, image_mapping, label_class_mapping)
        
    @staticmethod
    def merge_projects(API_class_src, API_class_dst, project_ids_src, project_id_dst):
        for project_id_src in project_ids_src:
            Utils.copy_project(API_class_src, API_class_dst, project_id_src, project_id_dst)