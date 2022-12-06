# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

##########################################################################
# object_storage_document_classification_demo.py
#
# Supports Python 3
##########################################################################
# Info:
# Object Storage Document Classification Processor Job creation using OCI AI Document Understanding service.
#
##########################################################################
# Application Command line(no parameter needed)
# python object_storage_document_classification_demo.py
##########################################################################

"""
This python script provides an example of how to use OCI Document Understanding Service document classification feature.

The configuration file used by service clients will be sourced from the default location (~/.oci/config) and the
CONFIG_PROFILE profile will be used.

The sample attempts to classify a document located in object storage.

"""
import oci
import uuid
import base64

# Setup basic variables
# Auth Config
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

# Compartment where processor job will be created
COMPARTMENT_ID = "<enter-your-compartment-ocid-here"  # e.g. "ocid1.compartment.oc1..aaaaaaaae5j73axsja5fnahbn23ilop3ynjkcg77mcvgryddz4pkh2t5ppaq";

def create_processor_job_callback(times_called, response):
    print("Waiting for processor lifecycle state to go into succeeded state:", response.data)

# Generate Document classification Feature
document_classification_feature = oci.ai_document.models.DocumentClassificationFeature()

# Setup input location where document being processed is stored.
object_location = oci.ai_document.models.ObjectLocation()
object_location.namespace_name = "<enter-your-objectstorage-namespsace-here>"  # e.g. "axhh9gizbq5x"
object_location.bucket_name = "<enter-your-bucket-name-here>"  # e.g "demo_examples"
object_location.object_name = "<enter-your-object-name-here>"  # e.g "document_classification_demo.pdf"

# Setup the output location where processor job results will be created
output_location = oci.ai_document.models.OutputLocation()
output_location.namespace_name = "<enter-your-objectstorage-namespsace-here>"  # e.g. "axk2tfhlrens"
output_location.bucket_name = "<enter-your-bucket-name-here>"  # e.g "output"
output_location.prefix = "<enter-your-prefix-here>"  # e.g "demo"

# Create a processor_job for document_classification_detection feature
create_processor_job_details_document_classification_detection = oci.ai_document.models.CreateProcessorJobDetails(
                                                display_name=str(uuid.uuid4()),
                                                compartment_id=COMPARTMENT_ID,
                                                input_location=oci.ai_document.models.ObjectListInlineInputLocation(object_locations=[object_location]),
                                                output_location=output_location,
                                                processor_config=oci.ai_document.models.GeneralProcessorConfig(features=[document_classification_feature]))

print("Calling create_processor with create_processor_job_details_document_classification_detection:", create_processor_job_details_document_classification_detection)
create_processor_response = aiservicedocument_client.create_processor_job_and_wait_for_state(
    create_processor_job_details=create_processor_job_details_document_classification_detection,
    wait_for_states=[oci.ai_document.models.ProcessorJob.LIFECYCLE_STATE_SUCCEEDED],
    waiter_kwargs={"wait_callback": create_processor_job_callback})

print("processor call succeeded with status: {} and request_id: {}.".format(create_processor_response.status, create_processor_response.request_id))
processor_job: oci.ai_document.models.ProcessorJob = create_processor_response.data
print("create_processor_job_details_document_classification_detection response: ", create_processor_response.data)

print("Getting result json from the output_location")
object_storage_client = oci.object_storage.ObjectStorageClient(config=config)
get_object_response = object_storage_client.get_object(namespace_name=output_location.namespace_name,
                                                       bucket_name=output_location.bucket_name,
                                                       object_name="{}/{}/{}_{}/results/{}.json".format(
                                                           output_location.prefix, processor_job.id,
                                                           object_location.namespace_name,
                                                           object_location.bucket_name,
                                                           object_location.object_name))

print(str(get_object_response.data.content.decode()))